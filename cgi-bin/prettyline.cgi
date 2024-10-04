#!/usr/bin/perl -w
#
# prettyline.pl
# -------------
# split up lines to make them look nice
#
#  Copyright (C) 2002 Swaine Chen and William Lee
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
$width = 80;
while (defined ($in = <>)) {
  if ($in =~ m/^>/) { print $in; next; }
  chomp $in;
  for ($i = 0; $i < length $in; $i += $width) {
    print substr($in, $i, $width), "\n";
  }
}
