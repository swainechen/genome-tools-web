#!/usr/bin/perl -w

# Initialization stuff
# --------------------
################################################
# These variables are set by read_web_config now
# default values are here

$conf_perl_include = "/var/www/genome-tools/cgi-bin/lib";
$conf_perl_bin = "/var/www/genome-tools/cgi-bin";
$conf_real_tmp_file_path = "/var/www/genome-tools/tmp";
$conf_html_tmp_file_path = "/genome-tools/tmp";
$conf_log_usage = 1;
$conf_log_ip = 0;
################################################

use vars qw($conf_log_dir $conf_real_cgi_bin);
&read_web_config();
use CGI;
$query = new CGI;

$commandLinePrefix = "/usr/bin/perl -I$conf_perl_include $conf_perl_bin";
$pretty = $conf_real_cgi_bin."/prettyline.cgi";
$chompme = $conf_perl_bin."/chompnewline.pl";

print $query->header;
print "<PRE>\n";

&cleanup;

# --------------------
# Open Temp File
# --------------------
sub GetTempFilename {
  my ($suffix) = @_;
  my $tmpFile;
  do {
    $tmpFile = time() . RandString(10) . $query->remote_host() . ".$suffix";
  } until (!-e "$conf_real_tmp_file_path/$tmpFile");
  return $tmpFile;
}
$tmpFile = GetTempFilename('tmp');
open(TMPFILE, ">$conf_real_tmp_file_path/$tmpFile") || die "Could not open temp file $tmpFile for writing";
# --------------------

$program = $query->param('program');

$orgcode = $query->param('orgcode');

if ($program eq 'Position') {
  $input = GetInput('positionInput');
  print TMPFILE $input;
  close(TMPFILE);
  $output = `$commandLinePrefix/position.pl $orgcode < $conf_real_tmp_file_path/$tmpFile`;
  print "$output\n";
  &LogUsage($orgcode, "position.pl");
} elsif ($program eq 'Nearest ORF') {
  $input = GetInput('nearestorfInput');
  print TMPFILE $input;
  close(TMPFILE);
  $output = `$commandLinePrefix/nearestorf.pl $orgcode < $conf_real_tmp_file_path/$tmpFile`;
  print "$output\n";
  &LogUsage($orgcode, "nearestorf.pl");
} elsif ($program eq 'Molecular Weight') {
  $input = GetInput('mwInput');
  print TMPFILE $input;
  close(TMPFILE);
  $output = `$chompme $conf_real_tmp_file_path/$tmpFile | $commandLinePrefix/MW.pl`;
  print "$output\n";
  &LogUsage($orgcode, "MW.pl");
} elsif ($program eq 'Subsequence') {
  $input = GetInput('subseqStart') . " " . GetInput('subseqLength');
  print TMPFILE $input;
  close(TMPFILE);
  $output = `$commandLinePrefix/subseq.pl $orgcode < $conf_real_tmp_file_path/$tmpFile | $pretty`;
  print "$output\n";
  &LogUsage($orgcode, "subseq.pl");
} elsif ($program eq 'Subsequence2') {
  $input = GetInput('subseq2Start') . ".." . GetInput('subseq2End');
  print TMPFILE $input;
  close(TMPFILE);
  $output = `$commandLinePrefix/subseq.pl $orgcode < $conf_real_tmp_file_path/$tmpFile | $pretty`;
  print "$output\n";
  &LogUsage($orgcode, "subseq.pl");
} elsif ($program eq 'Reverse Complement') {
  $input = GetInput('revcompInput');
  print TMPFILE $input;
  close(TMPFILE);
  $output = `$chompme $conf_real_tmp_file_path/$tmpFile | $commandLinePrefix/revcomp.pl  | $pretty`;
  print "$output\n";
  &LogUsage($orgcode, "revcomp.pl");
} elsif ($program eq 'Surround') {
  $input = GetInput('surroundPos') . " " . GetInput('surroundOffset');
  print TMPFILE $input;
  close(TMPFILE);
  $output = `$commandLinePrefix/surround.pl $orgcode < $conf_real_tmp_file_path/$tmpFile | $pretty`;
  print "$output\n";
  &LogUsage ($orgcode, "surround.pl");
} elsif ($program eq 'GATC') {
  $input = GetInput('gatcInput');
  print TMPFILE $input;
  close(TMPFILE);
  $output = `$chompme $conf_real_tmp_file_path/$tmpFile | $commandLinePrefix/gatc.pl`;
  print "$output\n";
  &LogUsage ($orgcode, "gatc.pl");
} elsif ($program eq 'Codon Usage') {
  $input = GetInput('codonInput');
  print TMPFILE $input;
  close(TMPFILE);
  $output = `$chompme $conf_real_tmp_file_path/$tmpFile | $commandLinePrefix/codonuse.pl`;
  print "$output\n";
  &LogUsage ($orgcode, "codonuse.pl");
} elsif ($program eq 'ORF Region') {
  $input = GetInput('orfregionORF') . (length($query->param('orfregionUp')) > 0 ? " " . $query->param('orfregionUp') : " 0") . (length($query->param('orfregionDown')) > 0 ? " " . $query->param('orfregionDown') : "");
  print TMPFILE $input;
  close(TMPFILE);
  $output = `$commandLinePrefix/orfregion.pl $orgcode < $conf_real_tmp_file_path/$tmpFile | $pretty`;
  print "$output\n";
  &LogUsage ($orgcode, "orfregion.pl");
} elsif ($program eq 'Translate') {
  $input = GetInput('transInput');
  print TMPFILE $input;
  close(TMPFILE);
  $transCommandline = '';
#  if (!($query->param("transFlagsingle") =~ m/single/m))     { $transCommandline .= '-nosingle '; }
#  if (!($query->param("transFlagtriple") =~ m/triple/m))     { $transCommandline .= '-notriple '; }
#  if (!($query->param("transFlagsix") =~ m/six/m))           { $transCommandline .= '-nosix '; }
#  if (!($query->param("transFlagsequence") =~ m/sequence/m)) { $transCommandline .= '-nosequence '; }
  if (!defined($query->param("transFlagsingle")))             { $transCommandline .= '-nosingle '; }
  if (!defined($query->param("transFlagtriple")))             { $transCommandline .= '-notriple '; }
  if (!defined($query->param("transFlagsix")))                { $transCommandline .= '-nosix '; }
  if (!defined($query->param("transFlagsequence")))           { $transCommandline .= '-nosequence '; }
  $output = `$chompme $conf_real_tmp_file_path/$tmpFile | $commandLinePrefix/translate.pl $transCommandline | $pretty`;
  print "$output\n";
  &LogUsage ($orgcode, "translate.pl");
} elsif ($program eq 'Genome Sequence') {
  close(TMPFILE);
  $output = `$commandLinePrefix/print-genome-file.pl $orgcode -suffix fna.oneline | $pretty`;
  print "$output\n";
  &LogUsage ($orgcode, "print-fna");
} elsif ($program eq 'Gene Sequences') {
  close(TMPFILE);
  $output = `$commandLinePrefix/print-genome-file.pl $orgcode -suffix ffn.oneline | $pretty`;
  print "$output\n";
  &LogUsage ($orgcode, "print-ffn");
} elsif ($program eq 'Protein Sequences') {
  close(TMPFILE);
  $output = `$commandLinePrefix/print-genome-file.pl $orgcode -suffix faa.oneline | $pretty`;
  print "$output\n";
  &LogUsage ($orgcode, "print-faa");
} elsif ($program eq 'Intergenics') {
  close(TMPFILE);
  $output = `$commandLinePrefix/print-genome-file.pl $orgcode -suffix fna.intergenic | $pretty`;
  print "$output\n";
  &LogUsage ($orgcode, "print-intergenic");
} elsif ($program eq 'GATC Content') {
  close(TMPFILE);
  $output = `$commandLinePrefix/print-genome-file.pl $orgcode -suffix fna.gatc`;
  print "$output\n";
  &LogUsage ($orgcode, "print-gatc");
} elsif ($program eq 'Total Codon Usage') {
  close(TMPFILE);
  $output = `$commandLinePrefix/print-genome-file.pl $orgcode -suffix ffn.codonusage`;
  print "$output\n";
  &LogUsage ($orgcode, "print-codonusage");
} elsif ($program eq 'Coding Region Table') {
  close(TMPFILE);
  $output = `$commandLinePrefix/print-genome-file.pl $orgcode -suffix ptt`;
  print "$output\n";
  &LogUsage ($orgcode, "print-ptt");
} elsif ($program eq 'Changes from GenBank') {
  close(TMPFILE);
  $output = `$commandLinePrefix/print-genome-file.pl $orgcode -suffix ptt-sanemaker.pl`;
  if (length($output) < 1) {
    print "No changes were made to the GenBank annotation.";
  } else {
    print "$output\n";
  }
  &LogUsage ($orgcode, "print-ptt-sanemaker");
} elsif ($program eq 'Graphic-Gene organization') {
  $input = GetInput('psgraphicLoc') . " " . GetInput('psgraphicLength');
  print TMPFILE $input;
  close(TMPFILE);
  $tmpPSFile = GetTempFilename ("ps");
  $tmpGIFFile = GetTempFilename ("gif");
  print "<p><a href=\"$conf_html_tmp_file_path/$tmpPSFile\">Download PostScript file</a> (which can be used to modify text/colors or make high resolution images)<p><p>\n";
  $output = `$commandLinePrefix/gene-graph.pl $orgcode -o $conf_real_tmp_file_path/$tmpPSFile < $conf_real_tmp_file_path/$tmpFile`;
  $output .= `convert $conf_real_tmp_file_path/$tmpPSFile $conf_real_tmp_file_path/$tmpGIFFile`;
  print "<img src=\"$conf_html_tmp_file_path/$tmpGIFFile\">\n";
  &LogUsage ($orgcode, "ps-graphic");
} elsif ($program eq 'Circular-Chromosome location') {
  $input = GetInput('pscircularInput');
  print TMPFILE $input;
  close(TMPFILE);
  $tmpPSFile = GetTempFilename ("ps");
  $tmpGIFFile = GetTempFilename ("gif");
  $output = `$commandLinePrefix/circular-graph.pl $orgcode -o $conf_real_tmp_file_path/$tmpPSFile < $conf_real_tmp_file_path/$tmpFile`;
  $output .= `convert $conf_real_tmp_file_path/$tmpPSFile $conf_real_tmp_file_path/$tmpGIFFile`;
  print "<p><a href=\"$conf_html_tmp_file_path/$tmpPSFile\">Download PostScript file</a> (which can be used to modify text/colors or make high resolution images)<p><p>\n";
  print "<img src=\"$conf_html_tmp_file_path/$tmpGIFFile\">\n";
  &LogUsage ($orgcode, "ps-circular");
} elsif ($program eq 'BLAST') {
  $input = GetInput('BlastInput');
  $type = GetInput('BlastType');
  $blastm = GetInput('BlastM');
  $blastb = GetInput('BlastB');
  print TMPFILE $input;
  close(TMPFILE);
  $output = `$commandLinePrefix/slc-$type $orgcode -m $blastm -b $blastb $conf_real_tmp_file_path/$tmpFile`;
  print $output;
}

# --------------------
# Remove Temp File
# --------------------
unlink $tmpFile;
# --------------------
print "</PRE>\n";


# GetInput
# --------
# Subroutine that sanitzes the input from a textarea field a bit so it
# handles newlines correctly
sub GetInput {
  my ($fieldName) = @_;

  if (length($query->param("$fieldName")) < 1) {
    print "<font size=+2><font color=red>Error: invalid input for field $fieldName</font>\n";
    print "Please return to <a href=\"http://genome-tools.sourceforge.net/\">Genome Tools</a>.</font>\n";
    exit(-1);
  }
  if (length($query->param("$fieldName")) > 10000) {
    print "<font size=+2><font color=red>Error: invalid input for field $fieldName (more than 10kb)</font>\n";
    print "Please return to <a href=\"http://genome-tools.sourceforge.net/\">Genome Tools</a>.</font>\n";
    exit(-1);
  }

  my $inputString = $query->param("$fieldName");

  my @inputArray = split /\s+/, $inputString;

  return (join("\n", @inputArray));
}

# LogUsage
# --------
# Subroutine to log usage by program.
# Log file will be in F:\Default Web Site Logs\genome-tools
# Log file will be named by date
# Each line will have a date, time, hostname/IP address, orgcode, and program on it
sub LogUsage {
  if (!$conf_log_usage) { return; }
  my @orgcode_and_program = @_;
  my @localtime = localtime(time);
  my $date = substr('0'.$localtime[5], -2);
  $date .= substr('0'.($localtime[4]+1), -2);
  $date .= substr('0'.$localtime[3], -2);			# year, month, day
  my $time = substr($localtime[2], -2).":";
  $time .= substr('0'.$localtime[1], -2).":";
  $time .= substr('0'.$localtime[0], -2);		# hour, min, sec

  my $remoteIP;
  if ($conf_log_ip) { $remoteIP = $query->remote_host(); }
  else { $remoteIP = "0.0.0.0"; }

  my $logfile = "$conf_log_dir/gt$date.log";
  if (-e $logfile) { open (LOG, ">>$logfile"); } else { open (LOG, ">$logfile"); }
  print LOG join ("\t", $date, $time, $remoteIP, @orgcode_and_program), "\n";
  close LOG;
}

# RandString
# ----------
# Utility function to generate a random string of a specified length.
#
sub RandString {
  my ($numChars) = @_;
  my $str = '';
  my @chr = qw(a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z);
  srand (time ^ $$ ^ unpack "%L*", `ps axww | gzip`);
  for (my $i = 0; $i < $numChars; $i++) {
    $str .= $chr[rand @chr];
  }
  return ($str);
}

# Cleanup
# -------
# clean up temp files that are older than 20 minutes
sub cleanup {
  my @files = `/bin/ls -1 $conf_real_tmp_file_path/*`;
  foreach my $file (@files) {
    if ($file =~ m/(\d+)[a-zA-Z]/) {
      my $createtime = $1;
      if (time() - $createtime > 1200 || time() - $createtime < 0) {
        my $return = `rm -f $file`;
      }
    }
  }
}

sub read_web_config {
  open CONF, "web.conf";
  while (<CONF>) {
    next if /^#/;
    chomp;
    my @f = split /\s*=\s*/, $_;
    ${$f[0]} = $f[1];
  }
  close CONF;
}
