# Laboratory works on automata theory

laboratory course on automata theory NRNU MEPhI

## Lab 1

Parsing the name of the program and its keys:

```
text.exe -key1 --key2
```

Using methods:

1)Lex

2)Regex

3)Smc

## Lab 2

Сreate a graph according to the received regular expression

```
a+(<qwe>ab|(ba){,2})<qwe>{1,3}
```

## Lab 3

Writing your own program text interpreter

```
function mul(int r int i)
    begin
    int res set 0;
    int j set i;
    do
        begin
        res set res add r;
        j set j sub 1;
        end
    while j first larger 0;
    end
return res;

function power(int x int y)
    begin
    int r set 1;
    int i set 0;
    do
        begin
        r set mul(r x);
        i set i add 1;
        end
    while i first smaller y;
    end
return r;

function work()
    begin
    int x set 2, y set 5;
    int ans set power(x y);
    int x1 set 3;
    end
return 0;
```