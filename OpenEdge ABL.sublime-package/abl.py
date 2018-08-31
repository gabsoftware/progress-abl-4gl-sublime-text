import sublime
import sublime_plugin

import subprocess
import threading
import os

import tempfile
import json
import uuid

class AblCommand(sublime_plugin.WindowCommand):

    encoding = 'utf-8'
    killed = False
    proc = None
    panel = None
    panel_lock = threading.Lock()

    def is_enabled(self, lint=False, integration=False, kill=False):
        # The Cancel build option should only be available
        # when the process is still running
        if kill:
            return self.proc is not None and self.proc.poll() is None
        return True

    def run(self, action="check_syntax", kill=False):
        if kill:
            if self.proc:
                self.killed = True
                self.proc.terminate()
            return

        view = self.window.active_view()
        vars = self.window.extract_variables()
        
        view_settings = view.settings()
        working_dir = vars['file_path']
        project_dir, project_file = os.path.split(self.window.project_file_name())
        
        # A lock is used to ensure only one thread is
        # touching the output panel at a time
        with self.panel_lock:
            # Creating the panel implicitly clears any previous contents
            self.panel = self.window.create_output_panel('exec')

            settings = self.panel.settings()
            settings.set(
                'result_file_regex',
                r'(?:^(.+?):([0-9]+):([0-9]+)\s(.+)$)*'
            )
            settings.set('result_base_dir', working_dir)

            self.window.run_command('show_panel', {'panel': 'output.exec'})

        if self.proc is not None:
            self.proc.terminate()
            self.proc = None

        abl_p = os.path.join(sublime.cache_path(), 'OpenEdge ABL', 'abl.p')
        if not os.path.exists(abl_p):
            with open(abl_p, 'w') as outfile:
                outfile.write(sublime.load_resource('Packages/OpenEdge ABL/abl.p'))

        abl_settings = view_settings.get('abl');

        # Resolve relative paths to project
        propath = abl_settings['propath']
        for i, path in enumerate(propath):
            if not os.path.isabs(path):
                abl_settings['propath'][i] = os.path.join(project_dir, path)

        if not os.path.isabs(abl_settings['pf']):
            abl_settings['pf'] = os.path.join(project_dir, abl_settings['pf'])

        abl_settings['action'] = action

        if action == 'check_syntax' or action == 'compile' or action == 'run':
            abl_settings['filename'] = os.path.join(vars['file_path'], vars['file_name'])

        abl_settings_file = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + '.json')
        with open(abl_settings_file, 'w') as outfile:
            json.dump(abl_settings, outfile)    

        _progres = os.path.join(abl_settings['dlc'], 'bin', '_progres')
        if (os.name != "posix"):
            _progres += ".exe" # Does windows work without this? Who knows

        args = [_progres, '-1', '-b']

        # Run the entry point
        args.append('-p')
        args.append(abl_p)

        # Set the PF file
        pf_file = abl_settings['pf']
        args.append('-pf')
        if os.path.isabs(pf_file):
            args.append(pf_file)
        else:
            args.append(os.path.join(project_dir, pf_file))
        
        # Set the PARAM
        args.append('-param')
        args.append(abl_settings_file)
        
        abl_env = os.environ.copy()
        abl_env["DLC"] = abl_settings['dlc']
        abl_env["PROMSGS"] = os.path.join(abl_settings['dlc'], 'promsgs')

        if (os.name == "posix"):
            abl_env["TERM"] = 'xterm'

        self.proc = subprocess.Popen(
            args,
            env=abl_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=working_dir
        )
        self.killed = False

        thread = threading.Thread(
            target=self.read_handle,
            args=(self.proc.stdout,)
        )
        thread.start()
        thread.join()

        if os.path.exists(abl_settings_file):
            os.remove(abl_settings_file)
        
    def finished(self):
        stylesheet = '''
            <style>
                div.error {
                    padding: 0.4rem 0 0.4rem 0.7rem;
                    margin: 0.2rem 0;
                    border-radius: 2px;
                }
                div.error span.message {
                    padding-right: 0.7rem;
                }
                div.error a {
                    text-decoration: inherit;
                    padding: 0.35rem 0.7rem 0.45rem 0.8rem;
                    position: absolute;
                    bottom: 0.05rem;
                    border-radius: 0 2px 2px 0;
                    font-weight: bold;
                }
                html.dark div.error a {
                    background-color: #00000018;
                }
                html.light div.error a {
                    background-color: #ffffff18;
                }
            </style>
        '''

        errs = self.panel.find_all_results_with_text()
        view = self.window.active_view()
        view.erase_phantoms ("abl")

        if len(errs) > 0 and  errs[0][3] != '':
            pt = view.text_point(errs[0][1] - 1, errs[0][2] - 1)

            view.add_phantom ("abl", sublime.Region(pt, view.line(pt).b), 
                '<body id=inline-error>' + stylesheet +
                    '<div class="error">' +
                    '<span class="message">' + errs[0][3] + '</span>' +
                    '<a href=hide>' + chr(0x00D7) + '</a></div>' +
                '</body>'
                , sublime.LAYOUT_BLOCK
                , on_navigate=self.on_phantom_navigate)     

    def on_phantom_navigate(self, url):
        view = self.window.active_view()
        view.erase_phantoms ("abl")

    def read_handle(self, handle):
        chunk_size = 2 ** 13
        out = b''
        while True:
            try:
                data = os.read(handle.fileno(), chunk_size)
                # If exactly the requested number of bytes was
                # read, there may be more data, and the current
                # data may contain part of a multibyte char
                out += data
                if len(data) == chunk_size:
                    continue
                if data == b'' and out == b'':
                    raise IOError('EOF')
                # We pass out to a function to ensure the
                # timeout gets the value of out right now,
                # rather than a future (mutated) version
                self.queue_write(out.decode(self.encoding))
                if data == b'':
                    raise IOError('EOF')
                out = b''
            except (UnicodeDecodeError) as e:
                msg = 'Error decoding output using %s - %s'
                self.queue_write(msg  % (self.encoding, str(e)))
                break
            except (IOError):
                if self.killed:
                    msg = 'Cancelled'
                else:
                    msg = 'Finished'
                sublime.set_timeout(self.finished, 1)
                self.queue_write('\n[%s]' % msg)
                break

    def queue_write(self, text):
        sublime.set_timeout(lambda: self.do_write(text), 1)

    def do_write(self, text):
        with self.panel_lock:
            self.panel.run_command('append', {'characters': text, 'force': True, 'scroll_to_end': True})
        
