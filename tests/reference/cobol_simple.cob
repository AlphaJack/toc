      *> ┌───────────────────────────────────────────────────────────────┐
      *> │ Contents of cobol_simple.cob                                  │
      *> ├───────────────────────────────────────────────────────────────┘
      *> │
      *> ├── Unique section
      *> │
      *> └───────────────────────────────────────────────────────────────

      *> ################################################################ Unique section
             *> setup the identification division
             IDENTIFICATION DIVISION.
             *> setup the program id
             PROGRAM-ID. HELLO.
             *> setup the procedure division (like 'main' function)
             PROCEDURE DIVISION.
               *> print a string
               DISPLAY 'WILLKOMMEN'.
             *> end our program
             STOP RUN.
