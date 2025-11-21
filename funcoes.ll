; ModuleID = "brasilscript"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define double @"soma"(double %"a", double %"b")
{
entry:
  %"a.1" = alloca double
  store double %"a", double* %"a.1"
  %"b.1" = alloca double
  store double %"b", double* %"b.1"
  ret double              0x0
}

define i32 @"main"()
{
entry:
  %"x" = alloca double
  store double              0x0, double* %"x"
  %"y" = alloca double
  store double              0x0, double* %"y"
  %"resultado" = alloca double
  store double              0x0, double* %"resultado"
  %".5" = call i32 (i8*, ...) @"printf"(i8* bitcast ([4 x i8]* @".str0" to i8*), double              0x0)
  ret i32 0
}

@".str0" = constant [4 x i8] c"%f\0a\00"