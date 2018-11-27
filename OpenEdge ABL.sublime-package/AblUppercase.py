import sublime
import sublime_plugin


class AblUppercaseCommand( sublime_plugin.TextCommand ):
   
    def run( self, edit, **kargs ):

        abl_settings = self.view.settings().get('abl')

        if abl_settings['uppercase_keywords']:
            # can't use `view.sel()[:]` because it gives an error `TypeError: an integer is required`
            selections   = [ cursor for cursor in self.view.sel() ]
            to_uppercase = []

            for sel in selections:

                if sel.end() > 0:
                    if self.view.substr( sel.end() - 1 ) == '(':
                        offset = 2
                    else:
                        offset = 1

                    #prev_item = self.view.extract_scope( sel.end() - offset )
                    scope = self.view.scope_name( sel.end() - offset )
                    begin = sel.end() - offset

                    while self.view.scope_name( begin ) == scope and begin > 0:
                        begin -= 1

                    prev_item = sublime.Region( begin, sel.end() )
                    to_uppercase.append( prev_item )

            self.view.sel().clear()
            self.view.sel().add_all( to_uppercase )
            self.view.run_command( 'upper_case' )

            self.view.sel().clear()
            self.view.sel().add_all( selections )
            
        self.view.run_command( 'insert', { 'characters': kargs["keystroke"] } )


class ScopeBeforeCursorEventListener( sublime_plugin.EventListener ):
    """
    Event listener used on the key binding `scope_before_cursor` available on the class's
    `UpperCasePreviousItemAndInsertSpaceCommand` documentation.
    """

    def on_query_context( self, view, key, operator, operand, match_all ):

        if key != 'scope_before_cursor':
            return None

        if operator not in ( sublime.OP_EQUAL, sublime.OP_NOT_EQUAL ):
            return None

        match = False

        for sel in view.sel():
            #print( max(0, sel.end() - 1) )

            if view.substr(sel.end() - 1) == '(':
                offset = 2
            else:
                offset = 1

            for op in operand:
                match = view.match_selector( max(0, sel.end() - offset ), op )
                #print( 'On 1º match: ', match )
                
                if match:
                    break

            if operator == sublime.OP_NOT_EQUAL:
                match = not match

            if match != match_all:
                break

        #print( 'match: ', match )
        return match