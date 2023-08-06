labelframe .f -text label1
set v 0
proc bg {} {
global v
incr v
after idle bg
}
entry .f.e -textvariable v
pack .f.e
pack .f
update
after 1000 bg
