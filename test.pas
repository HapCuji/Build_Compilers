PROGRAM HelloWorld;
VAR
   a : INTEGER;

FUNCTION F1: REAL;
VAR
   a : REAL;
   k : INTEGER;

   FUNCTION F2: INTEGER;
   VAR
      a, z : INTEGER;
   BEGIN {F2}
      F2 := 'test';
   END;  {F2}

BEGIN {F1}

END;  {F1}

BEGIN {HelloWorld}
   a := 10;
END.  {HelloWorld}