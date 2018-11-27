USING Progress.Json.ObjectModel.ObjectModelParser.
USING Progress.Json.ObjectModel.JsonObject.
USING Progress.Json.ObjectModel.JsonArray.

DEFINE VARIABLE oABLSettingsParser AS ObjectModelParser NO-UNDO.
DEFINE VARIABLE oABLSettings       AS JsonObject        NO-UNDO.
DEFINE VARIABLE oHooks             AS JsonObject        NO-UNDO.
DEFINE VARIABLE oPropath           AS JsonArray         NO-UNDO.
DEFINE VARIABLE oDBs               AS JsonArray         NO-UNDO.
DEFINE VARIABLE iDbs               AS INTEGER           NO-UNDO.
DEFINE VARIABLE iPropath           AS INTEGER           NO-UNDO.
DEFINE VARIABLE cSettingsData      AS LONGCHAR          NO-UNDO.
DEFINE VARIABLE cPropath           AS CHARACTER         NO-UNDO.
DEFINE VARIABLE cAction            AS CHARACTER         NO-UNDO.
DEFINE VARIABLE lCompiles          AS LOGICAL           NO-UNDO.

FIX-CODEPAGE(cSettingsData) = "UTF-8".
COPY-LOB FROM FILE SESSION:PARAMETER To cSettingsData.

oABLSettingsParser   = NEW ObjectModelParser().
oABLSettings         = CAST(oABLSettingsParser:Parse(cSettingsData), JsonObject).

cAction = oABLSettings:getCharacter("action":U).

/* If we had db's lets cnnect them */
IF oABLSettings:has("db":U)
THEN
DO:
  ASSIGN
    oDBs = oABLSettings:getJsonArray("db":U).

  DO iDbs = 1 TO oDBs:Length:
    CONNECT VALUE(oDBs:getCharacter(iDbs)).
  END.
END.

/* If we had a propath lets set it */
IF oABLSettings:has("propath":U)
THEN
DO:
  ASSIGN
    cPropath = "":U
    oPropath = oABLSettings:getJsonArray("propath":U).

  DO iPropath = 1 TO oPropath:Length:
    cPropath = cPropath + (IF iPropath = 1 THEN "":U ELSE ",":U) + oPropath:getCharacter(iPropath).
  END.

  PROPATH = cPropath.
END.

/* Fire off any hooks */
IF oABLSettings:has("hooks":U)
THEN
DO:
  oHooks = oABLSettings:getJsonObject("hooks":U).

  IF oHooks:has("pre":U)
  THEN
    RUN VALUE(oHooks:getCharacter("pre":U)) NO-ERROR. 

END.

CASE cAction:

  WHEN "check_syntax":U OR
  WHEN "compile":U
  THEN
    RUN abl_compile (INPUT (cAction = "compile":U), OUTPUT lCompiles).

  WHEN "run-batch":U OR
  WHEN "run-gui":U
  THEN
  DO:
    RUN abl_compile (INPUT TRUE, OUTPUT lCompiles).

    IF lCompiles
    THEN
      RUN abl_run.
  END.
END CASE.

QUIT.

PROCEDURE abl_compile:
  DEFINE INPUT  PARAMETER iplSave   AS LOGICAL   NO-UNDO.
  DEFINE OUTPUT PARAMETER oplErrors AS LOGICAL   NO-UNDO INITIAL TRUE.

  DEFINE VARIABLE cFileName   AS CHARACTER  NO-UNDO.
  DEFINE VARIABLE cXrefXml    AS CHARACTER  NO-UNDO.
  DEFINE VARIABLE cMessage    AS CHARACTER  NO-UNDO.
  DEFINE VARIABLE iMessage    AS INTEGER    NO-UNDO.

  cFileName = oABLSettings:getCharacter("filename":U).

  IF iplSave
  THEN
    COMPILE VALUE(cFileName) SAVE NO-ERROR.
  ELSE
  DO:
    cXrefXml = cFileName + ".xref".
  
    COMPILE VALUE(cFileName) XREF-XML VALUE(cXrefXml) NO-ERROR.
  END.

  IF COMPILER:NUM-MESSAGES > 0 THEN DO:

    ASSIGN 
      cMessage = ""
      oplErrors = FALSE.
  
    DO iMessage = 1 TO COMPILER:NUM-MESSAGES:
  
      ASSIGN cMessage =
        SUBSTITUTE( "&1:&2:&3 &4",
          COMPILER:GET-FILE-NAME  ( iMessage ),
          COMPILER:GET-ROW        ( iMessage ),
          COMPILER:GET-COLUMN     ( iMessage ),
          COMPILER:GET-MESSAGE    ( iMessage )
        )
      .
  
      IF iMessage < COMPILER:NUM-MESSAGES
      THEN
        PUT UNFORMATTED cMessage SKIP.
      ELSE
        PUT UNFORMATTED cMessage.
      
    END.
  END.

  FINALLY:
    IF cXrefXml <> ? AND cXrefXml <> "":U
    THEN
      OS-DELETE VALUE(cXrefXml).
  END FINALLY.
END PROCEDURE.

PROCEDURE abl_run:
  DEFINE VARIABLE cFileName   AS CHARACTER  NO-UNDO.
  DEFINE VARIABLE cMessage    AS CHARACTER  NO-UNDO.
  DEFINE VARIABLE iMessage    AS INTEGER    NO-UNDO.

  cFileName = oABLSettings:getCharacter("filename":U).

  RUN VALUE(cFileName).
END.
