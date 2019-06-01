Program lr3var21;
Var y:real;
	x:integer;
Begin
	Writeln('write your arg x = ');
	Readln(x);
	Case x of
		1..9999: y:=sqrt(x);
		0: y:=sqrt(x);
		-9999..-1:
		begin
			x:=-x;
			y:=sqrt(x);
		end;
	end;
	Writeln(y);
	Readln;
End.