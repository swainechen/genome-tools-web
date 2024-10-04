#!/usr/bin/perl -w

#
# variables set by web.conf file should be
# conf_html_root - i.e. the string after the server name for the whole website
# conf_real_root - i.e. where on the server the files are
# conf_html_cgi_bin - the string to request cgi-bin scripts
# conf_real_cgi_bin - the cgi-bin directory on the server
# conf_log_dir - the log directory on the server
# conf_show_graphics_tools - whether to show tools which output graphics
#

use vars qw($conf_perl_include $conf_html_cgi_bin $conf_real_cgi_bin $genbank_link $conf_show_graphics_tools $acknowledgement);
&read_web_config();
use CGI;
$query = new CGI;
print $query->header;
@news_date = localtime ((stat("$conf_real_root/news.html"))[9]);
$news_date = ($news_date[4]+1)."/".$news_date[3]."/".($news_date[5]+1900);

# BEGIN Genome Selection Table
if (!defined($query->param("orgcode")) || length($query->param("orgcode")) != 4) {
  &set_header;
  print $TABLE_HEADER;

  open(ORGMAP, "$conf_perl_include/org-map");

  $lastSpeciesName = "";
  $temporaryCounter = 0;
  while(defined($line = <ORGMAP>)) {
    @lineArray = split /\t/, $line;
    if ($lastSpeciesName eq "" || $temporaryCounter == 4) {
					# only show 4 cols to make it look nicer
        print "<tr>\n";
        $temporaryCounter = 0;
    } elsif ($lastSpeciesName ne $lineArray[5]) {
        print "</tr>\n<tr>";
        $temporaryCounter = 0;
    }
    $lastSpeciesName = $lineArray[5];
    print "<td><input type=radio name=orgcode value=$lineArray[0]";
    if ($lineArray[0] eq "uti8") { print " checked"; }
    print ">";
    print "<a href=\"$conf_html_cgi_bin/genome-tools-web-interface.cgi?orgcode=$lineArray[0]\"><i>$lineArray[5]</i> $lineArray[6]</a></td>\n";
    ++$temporaryCounter;
  }
  close(ORGMAP);
  print "<tr><td align=middle colspan=4><input type=submit value=\"Select Genome\"></td></tr>\n";
  print "</table></td></tr>\n";
# END Genome Selection Table
} else {
  $orgcode = $query->param("orgcode");
  open(ORGMAP, "$conf_perl_include/org-map");
  while(defined($line = <ORGMAP>)) {
    @lineArray = split /\t/, $line;
    if ($lineArray[0] eq $orgcode) {
      $genome_name = $lineArray[5];
      $sub_name = $lineArray[6];
      $genbank_link = $lineArray[7];
      print "<title>Genome-Tools - $genome_name $sub_name</title>\n";
      last;
    }
  }
  &set_tools;
  if ($conf_show_graphics_tools) { print $TOOLS_GRAPHICS; }
  else { print $TOOLS_NOGRAPHICS; }
}

&set_footer;
print $FOOTER;

##########################
# String definitions below
##########################

sub substitute_tags {
  my ($string) = @_;
  foreach my $configured_var (qw(conf_html_root conf_html_cgi_bin genome_name sub_name genbank_link acknowledgement news_date orgcode)) {
    next if (!defined $$configured_var);
    my $searchpattern = "__".uc($configured_var)."__";
    my $replacetext = $$configured_var;
    $string =~ s/$searchpattern/$replacetext/g;
  }
  return $string;
}

# BEGIN TABLE_HEADER definition
sub set_header {
$TABLE_HEADER = '
<title>Organism selection - genome-tools</title>
<body>
<center>
<h1><font face="Arial">Genome-Tools Web Interface</font></h1>
<table border=0 cellspacing=10>
<tr>
<td align=right>Genome-Tools Project Homepage:</td>
<td><a
href="https://github.com/swainechen/genome-tools">https://github.com/swainechen/genome-tools</a></td>
</tr>
<tr>
<td align=right>Genome-Tools Downloads:</td>
<td><a
href="https://github.com/swainechen/genome-tools/releases">
https://github.com/swainechen/genome-tools/releases</a></td>
</tr>
</table>
</center>
<form name=orgselect method=get action="__CONF_HTML_CGI_BIN__/genome-tools-web-interface.cgi">
<table border=4 width=100%><tr><td><table cellspacing=0 cellpadding=0 width=100%>
<tr>
<th colspan=4>Please select a genome:</th>
</tr>
';

$TABLE_HEADER = substitute_tags $TABLE_HEADER;
}
# END TABLE_HEADER definition

# BEGIN FOOTER definition
sub set_footer {
$FOOTER = '
</table>
</form>
<hr>
<a href="https://github.com/swainechen/genome-tools">Genome-Tools Project Homepage</a><br>
<a href="__CONF_HTML_ROOT__/disclaimer.html">Disclaimer</a><br>
<font face="Times New Roman">© </font>2002 Swaine Chen and William Lee<br>
<a href="mailto:slchen@gis.a-star.edu.sg">Feedback and comments</a>
<p>
If these tools help you in your research, please cite:<br>
Lee, W. and Chen, S.L. 2002. "Genome-Tools: A Flexible Package for Genome Sequence Analysis". Biotechniques 33(6):1334-41.<br>
<p>
__ACKNOWLEDGEMENT__
<p>

</body>
';

open (ACK, "$conf_real_root/acknowledgement.html");
my @temparray = <ACK>;
$acknowledgement = join "", @temparray;

$FOOTER = substitute_tags $FOOTER;
}
# END FOOTER definition

# BEGIN TOOLS definitions
sub set_tools {
# BEGIN TOOLS_GRAPHICS definition
$TOOLS_GRAPHICS = '
<script>
positionSample = ">Sample_sequence\nTTAANNNNNNNTTAA"
nearestorfSample = ">Sample_position\n457"
DNASample = ">Sample_DNA_sequence\nATGCGCGTACTGTTGATCGAGGATGACAGCGCGACGGCGCAGACCATCGAACTGATGCTGAAGTCTGAAGGCTTCAACGTCTATACGACGGATCTGGGTGAAGAAGGCGTCGATCTGGGCAAGATCTACGACTACGATCTTATCCTGCTCGACCTCAATCTTCCGGACATGAGCGGCATCGATGTTCTGCGCACCCTGCGGGTCGCGAAGATCAACACGCCCATCATGATCCTGTCGGGCTCGTCGGAAATCGACACCAAGGTCAAGACCTTCGCCGGCGGCGCCGACGACTACATGACCAAGCCGTTCCACAAGGACGAAATGATCGCCCGCATCCACGCGGTGGTCCGTCGTTCGAAGGGTCACGCCCAGTCGGTCATCAAGACCGGCGACATCGTGGTCAACCTGGACGCCAAGACGGTGGAAGTGAACGGCAACCGCGTTCACCTGACCGGCAAGGAGTACCAGATGCTGGAGCTCCTCTCCCTGCGCAAGGGTACGACCCTGACCAAGGAAATGTTCCTGAACCACCTGTACGGCGGCATGGACGAGCCGGAACTGAAGATCATCGACGTCTTCATCTGCAAGCTGCGCAAGAAGCTGGCCGCTTCGGCGCACGGCAAGCACCACATTGAGACGGTCTGGGGCCGCGGCTATGTGCTGCGCGACCCGAACGAGCAGGTTAACGCCGCCTGA"
ProteinSample = ">Sample_protein_sequence\nMRVLLIEDDSATAQTIELMLKSEGFNVYTTDLGEEGVDLGKIYDYDLILLDLNLPDMSGIDVLRTLRVAKINTPIMILSGSSEIDTKVKTFAGGADDYMTKPFHKDEMIARIHAVVRRSKGHAQSVIKTGDIVVNLDAKTVEVNGNRVHLTGKEYQMLELLSLRKGTTLTKEMFLNHLYGGMDEPELKIIDVFICKLRKKLAASAHGKHHIETVWGRGYVLRDPNEQVNAA"
coordSample = 457
pscircularSample = "50000\n-100000\n150000\n-200000"
</script>
<p><font size=+2>Current genome: <i>__GENOME_NAME__</i> __SUB_NAME__</font></p>
<form action="__CONF_HTML_CGI_BIN__/genome-tools-web-interface.cgi"><input type=submit value="<-- Return to Genome Select page"></form>
<table width=50% border=0>
<tr>
<td><a href="http://www.ncbi.nlm.nih.gov/genomeprj/__GENBANK_LINK__">NCBI Genome Page</a></td>
<td><a href="__CONF_HTML_ROOT__/help.html">Help</a></td>
</tr>
<tr>
<td colspan=3><font size=-1>Note: Please read and agree to the <a href="__CONF_HTML_ROOT__/disclaimer.html">disclaimer</a> before using any of these tools.</font></td>
</tr>
<tr bgcolor="cfcfcf">
<td colspan=3>
Tools which output graphics are highlighted with a gray background
</td>
</tr>
</table>
<table border=0>
<form method=post action="__CONF_HTML_CGI_BIN__/genome-tools-web-wrapper.cgi">
<input type=hidden name=orgcode value="__ORGCODE__">
<tr>
<td colspan=5><hr></td>
</tr>

<tr>
<th align=right>DNA or Protein Sequence(s) to BLAST (max 10kb):</th>
<td>
<textarea name=BlastInput rows="5" cols="50"></textarea>
<br>
<select name=BlastType>
  <option value="blastn" selected>blastn (DNA Input, DNA database)</option>
  <option value="blastx">blastx (DNA Input, Protein database)</option>
  <option value="tblastx">tblastx (DNA Input, DNA database)</option>
  <option value="blastp">blastp (Protein Input, Protein database)</option>
  <option value="tblastn">tblastn (Protein Input, DNA database)</option>
</select>
Format: <select name=BlastM>
           <option value="0", selected>Long</option>
           <option value="6">Short</option>
        </select>
Number of results: <input type="text" name="BlastB" length=5 value=1>
</td>
<td><input type=submit name=program value="BLAST"></td>
<td align=middle><input type=button onClick="BlastInput.value = DNASample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#blast">Help</a></td>
</tr>

<tr><td>&nbsp;</td><td></td><td></td></tr>

<tr>
<th align=right>DNA sequence(s) to find positions for:</th>
<td><textarea name=positionInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value=Position></td>
<td align=middle><input type=button onClick="positionInput.value = positionSample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#position">Help</a></td>
</tr>

<tr>
<th align=right>Position(s) to find nearest ORFs for:</th>
<td><textarea name=nearestorfInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="Nearest ORF"></td>
<td align=middle><input type=button onClick="nearestorfInput.value = nearestorfSample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#nearestorf">Help</a></td>
</tr>

<tr bgcolor="#cfcfcf">
<th align=right>Position(s) to draw on a circular map:</th>
<td><textarea name=pscircularInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="Circular-Chromosome location"></td>
<td align=middle><input type=button onClick="pscircularInput.value = pscircularSample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#ps-circular">Help</a></td>
</tr>

<tr>
<th align=right>Where on genome to find sequence:</th>

<td><table width=100%>
<tr>
<td align=right>Start: </td><td>
<input type=text name=subseqStart size="10"></td>
<td align=right colspan=2>Length: </td><td colspan=2>
<input type=text name=subseqLength size="10"></td>
</tr>
<tr>
<td align=right>Start: </td><td>
<input type=text name=subseq2Start size="10"></td>
<td align=right colspan=2>End: </td><td colspan=2>
<input type=text name=subseq2End size="10"></td>
</tr>
<tr>
<td align=right>Position: </td><td>
<input type=text name=surroundPos size="10"></td>
<td align=right colspan=2>Bases surrounding: </td><td colspan=2>
<input type=text name=surroundOffset size="10"></td>
</tr>
<tr>
<td align=right>Systematic gene name/number: </td><td><input type=text name=orfregionORF size="10"></td>
<td align=right># Bases Upstream: </td><td>
<input type=text name=orfregionUp size="10"></td>
<td align=right># Bases Downstream: </td><td>
<input type=text name=orfregionDown size="10"></td>
</table></td>

<td valign=middle><table width=100% height=100% border=0>
<tr><td valign=middle><input type=submit name=program value="Subsequence"></td></tr>
<tr><td valign=middle><input type=submit name=program value="Subsequence2"></td></tr>
<tr><td valign=middle><input type=submit name=program value="Surround"></td></tr>
<tr><td valign=middle><input type=submit name=program value="ORF Region"></td></tr>
</table></td>

<td valign=middle align=middle><table width=100% height=100% border=0>
<tr><td valign=middle align=middle><input type=button onClick="subseqStart.value = coordSample
subseqLength.value = 693" value="Sample"></td>
</tr>
<tr><td valign=middle align=middle><input type=button onClick="subseq2Start.value = coordSample
subseq2End.value = coordSample + 693" value="Sample"></td>
</tr>
<tr><td valign=middle align=middle><input type=button onClick="surroundPos.value = coordSample
surroundOffset.value = 200" value="Sample"></td>
</tr>
<tr><td valign=middle align=middle><input type=button onClick="orfregionORF.value = 2
orfregionUp.value = 150
orfregionDown.value = 100" value="Sample"></td>
</tr>
</table></td>

<td valign=middle align=middle><table width=100% height=100% border=0>
<tr><td valign=middle align=middle><a href="__CONF_HTML_ROOT__/help.html#subseq">Help</a></td></tr>
<tr><td valign=middle align=middle><a href="__CONF_HTML_ROOT__/help.html#surround">Help</a></td></tr>
<tr><td valign=middle align=middle><a href="__CONF_HTML_ROOT__/help.html#orfregion">Help</a></td></tr>
</table></td>

</tr>

<tr bgcolor="cfcfcf">
<th align=right>Section of genome to show gene organization for:</th>
<td><table width=100%>
  <tr>
    <td align=right>Position: </td><td>
    <input type=text name=psgraphicLoc size="10"></td>
    <td align=right colspan=2>Length: </td>
    <td colspan=2><input type=text name=psgraphicLength size="10"></td>
  </tr>
</table></td>
<td><input type=submit name=program value="Graphic-Gene organization"></td>
<td align=middle><input type=button onClick="psgraphicLoc.value = 3000
psgraphicLength.value = 5000" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#ps-graphic">Help</a></td>
</tr>

<tr>
<th align=right>DNA sequence(s) to calculate nucleotide content for:</th>
<td><textarea name=gatcInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="GATC"></td>
<td align=middle><input type=button onClick="gatcInput.value = DNASample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#gatc">Help</a></td>
</tr>

<tr>
<th align=right>DNA sequence(s) to calculate codon usage for:</th>
<td><textarea name=codonInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="Codon Usage"></td>
<td align=middle><input type=button onClick="codonInput.value = DNASample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#codonuse">Help</a></td>
</tr>

<tr>
<th align=right>DNA sequence(s) to translate:</th>
<td><textarea name=transInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="Translate"></td>
<td><input type=button onClick="transInput.value = DNASample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#translate">Help</a></td>
</tr>
<tr>
<td></td>
<td>
<input type=checkbox name=transFlagsingle value=single checked>One letter
<input type=checkbox name=transFlagtriple value=triple>Three letter
<input type=checkbox name=transFlagsix value=six>Six-frame
<input type=checkbox name=transFlagsequence value=sequence>Print DNA sequence </td>
</tr>

<tr>
<th align=right>Protein sequence(s) to calculate molecular weight for:</th>
<td><textarea name=mwInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="Molecular Weight"></td>
<td align=middle><input type=button onClick="mwInput.value = ProteinSample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#MW">Help</a></td>
</tr>

<tr>
<th align=right>DNA sequence(s) to reverse complement:</th>
<td><textarea name=revcompInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="Reverse Complement"></td>
<td align=middle><input type=button onClick="revcompInput.value = DNASample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#revcomp">Help</a></td>
</tr>

<tr>
<th align=right>View genome information:</th>
<td colspan=3>
  <input type=submit name=program value="Coding Region Table">
  <input type=submit name=program value="Genome Sequence">
  <input type=submit name=program value="Gene Sequences">
  <input type=submit name=program value="Protein Sequences">
  <input type=submit name=program value="Intergenics">
  <input type=submit name=program value="GATC Content">
  <input type=submit name=program value="Total Codon Usage">
  <input type=submit name=program value="Changes from GenBank">
</td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#files">Help</a></td>
</tr>

<tr>
<td align=right><a href="__CONF_HTML_ROOT__/help.html">Help!</a></td>
<td colspan=4><input type=reset></td>
</tr>
<br>
';
# END TOOLS_GRAPHICS definition

# BEGIN TOOLS_NOGRAPHICS definition
$TOOLS_NOGRAPHICS = '
<script>
positionSample = ">Sample_sequence\nTTAANNNNNNNTTAA"
nearestorfSample = ">Sample_position\n457"
DNASample = ">Sample_DNA_sequence\nATGCGCGTACTGTTGATCGAGGATGACAGCGCGACGGCGCAGACCATCGAACTGATGCTGAAGTCTGAAGGCTTCAACGTCTATACGACGGATCTGGGTGAAGAAGGCGTCGATCTGGGCAAGATCTACGACTACGATCTTATCCTGCTCGACCTCAATCTTCCGGACATGAGCGGCATCGATGTTCTGCGCACCCTGCGGGTCGCGAAGATCAACACGCCCATCATGATCCTGTCGGGCTCGTCGGAAATCGACACCAAGGTCAAGACCTTCGCCGGCGGCGCCGACGACTACATGACCAAGCCGTTCCACAAGGACGAAATGATCGCCCGCATCCACGCGGTGGTCCGTCGTTCGAAGGGTCACGCCCAGTCGGTCATCAAGACCGGCGACATCGTGGTCAACCTGGACGCCAAGACGGTGGAAGTGAACGGCAACCGCGTTCACCTGACCGGCAAGGAGTACCAGATGCTGGAGCTCCTCTCCCTGCGCAAGGGTACGACCCTGACCAAGGAAATGTTCCTGAACCACCTGTACGGCGGCATGGACGAGCCGGAACTGAAGATCATCGACGTCTTCATCTGCAAGCTGCGCAAGAAGCTGGCCGCTTCGGCGCACGGCAAGCACCACATTGAGACGGTCTGGGGCCGCGGCTATGTGCTGCGCGACCCGAACGAGCAGGTTAACGCCGCCTGA"
ProteinSample = ">Sample_protein_sequence\nMRVLLIEDDSATAQTIELMLKSEGFNVYTTDLGEEGVDLGKIYDYDLILLDLNLPDMSGIDVLRTLRVAKINTPIMILSGSSEIDTKVKTFAGGADDYMTKPFHKDEMIARIHAVVRRSKGHAQSVIKTGDIVVNLDAKTVEVNGNRVHLTGKEYQMLELLSLRKGTTLTKEMFLNHLYGGMDEPELKIIDVFICKLRKKLAASAHGKHHIETVWGRGYVLRDPNEQVNAA"
coordSample = 457
</script>
<p><font size=+2>Current genome: <i>__GENOME_NAME__</i> __SUB_NAME__</font></p>
<form action="__CONF_HTML_CGI_BIN__/genome-tools-web-interface.cgi"><input type=submit value="<-- Return to Genome Select page"></form>
<table width=50% border=0>
<tr>
<td><a href="http://www.ncbi.nlm.nih.gov/cgi-bin/Entrez/framik?db=Genome&gi=__GENBANK_LINK__">NCBI Genome Page</a></td>
<td>The NCBI blast link is broken</td>
<td><a href="__CONF_HTML_ROOT__/help.html">Help</a></td>
</tr>
<tr>
<td colspan=3><font size=-1>Note: Please read and agree to the <a href="__CONF_HTML_ROOT__/disclaimer.html">disclaimer</a> before using any of these tools.</font></td>
</tr>
</table>
<table border=0>
<form method=post action="__CONF_HTML_CGI_BIN__/genome-tools-web-wrapper.cgi">
<input type=hidden name=orgcode value="__ORGCODE__">
<tr>
<td colspan=5><hr></td>
</tr>

<tr>
<th align=right>DNA sequence(s) to find positions for:</th>
<td><textarea name=positionInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value=Position></td>
<td align=middle><input type=button onClick="positionInput.value = positionSample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#position">Help</a></td>
</tr>

<tr>
<th align=right>Position(s) to find nearest ORFs for:</th>
<td><textarea name=nearestorfInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="Nearest ORF"></td>
<td align=middle><input type=button onClick="nearestorfInput.value = nearestorfSample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#nearestorf">Help</a></td>
</tr>

<tr>
<th align=right>Where on genome to find sequence:</th>

<td><table width=100%>
<tr>
<td align=right>Start: </td><td>
<input type=text name=subseqStart size="10"></td>
<td align=right colspan=2>Length: </td><td colspan=2>
<input type=text name=subseqLength size="10"></td>
</tr>
<tr>
<td align=right>Position: </td><td>
<input type=text name=surroundPos size="10"></td>
<td align=right colspan=2>Bases surrounding: </td><td colspan=2>
<input type=text name=surroundOffset size="10"></td>
</tr>
<tr>
<td align=right>Systematic gene name/number: </td><td><input type=text name=orfregionORF size="10"></td>
<td align=right># Bases Upstream: </td><td>
<input type=text name=orfregionUp size="10"></td>
<td align=right># Bases Downstream: </td><td>
<input type=text name=orfregionDown size="10"></td>
</table></td>

<td valign=middle><table width=100% height=100% border=0>
<tr><td valign=middle><input type=submit name=program value="Subsequence"></td></tr>
<tr><td valign=middle><input type=submit name=program value="Surround"></td></tr>
<tr><td valign=middle><input type=submit name=program value="ORF Region"></td></tr>
</table></td>

<td valign=middle align=middle><table width=100% height=100% border=0>
<tr><td valign=middle align=middle><input type=button onClick="subseqStart.value = coordSample
subseqLength.value = 693" value="Sample"></td>
</tr>
<tr><td valign=middle align=middle><input type=button onClick="surroundPos.value = coordSample
surroundOffset.value = 200" value="Sample"></td>
</tr>
<tr><td valign=middle align=middle><input type=button onClick="orfregionORF.value = 2
orfregionUp.value = 150
orfregionDown.value = 100" value="Sample"></td>
</tr>
</table></td>

<td valign=middle align=middle><table width=100% height=100% border=0>
<tr><td valign=middle align=middle><a href="__CONF_HTML_ROOT__/help.html#subseq">Help</a></td></tr>
<tr><td valign=middle align=middle><a href="__CONF_HTML_ROOT__/help.html#surround">Help</a></td></tr>
<tr><td valign=middle align=middle><a href="__CONF_HTML_ROOT__/help.html#orfregion">Help</a></td></tr>
</table></td>

</tr>

<tr>
<th align=right>DNA sequence(s) to calculate nucleotide content for:</th>
<td><textarea name=gatcInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="GATC"></td>
<td align=middle><input type=button onClick="gatcInput.value = DNASample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#gatc">Help</a></td>
</tr>

<tr>
<th align=right>DNA sequence(s) to calculate codon usage for:</th>
<td><textarea name=codonInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="Codon Usage"></td>
<td align=middle><input type=button onClick="codonInput.value = DNASample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#codonuse">Help</a></td>
</tr>

<tr>
<th align=right>DNA sequence(s) to translate:</th>
<td><textarea name=transInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="Translate"></td>
<td><input type=button onClick="transInput.value = DNASample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#translate">Help</a></td>
</tr>
<tr>
<td></td>
<td>
<input type=checkbox name=transFlagsingle value=single checked>One letter
<input type=checkbox name=transFlagtriple value=triple>Three letter
<input type=checkbox name=transFlagsix value=six>Six-frame
<input type=checkbox name=transFlagsequence value=sequence>Print DNA sequence </td>
</tr>

<tr>
<th align=right>Protein sequence(s) to calculate molecular weight for:</th>
<td><textarea name=mwInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="Molecular Weight"></td>
<td align=middle><input type=button onClick="mwInput.value = ProteinSample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#MW">Help</a></td>
</tr>

<tr>
<th align=right>DNA sequence(s) to reverse complement:</th>
<td><textarea name=revcompInput rows="5" cols="50"></textarea></td>
<td><input type=submit name=program value="Reverse Complement"></td>
<td align=middle><input type=button onClick="revcompInput.value = DNASample" value="Sample"></td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#revcomp">Help</a></td>
</tr>

<tr>
<th align=right>View genome information:</th>
<td colspan=3>
  <input type=submit name=program value="Intergenics">
  <input type=submit name=program value="GATC Content">
  <input type=submit name=program value="Total Codon Usage">
  <input type=submit name=program value="Coding Region Table">
  <input type=submit name=program value="Changes from GenBank">
</td>
<td align=middle><a href="__CONF_HTML_ROOT__/help.html#files">Help</a></td>
</tr>

<tr>
<td align=right><a href="__CONF_HTML_ROOT__/help.html">Help!</a></td>
<td colspan=4><input type=reset></td>
</tr>
<br>
';
# END TOOLS_NOGRAPHICS definition

$TOOLS_GRAPHICS = substitute_tags $TOOLS_GRAPHICS;
$TOOLS_NOGRAPHICS = substitute_tags $TOOLS_NOGRAPHICS;
}
# end of TOOLS definitions

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
