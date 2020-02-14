#!/usr/bin/perl -w
# map_panther.pl - Generic mapping program

use YAML::XS 'LoadFile';

my %FORM;
if ($ENV{'REQUEST_METHOD'} eq 'GET') {
  @pairs = split(/&/, $ENV{'QUERY_STRING'});
} elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
  read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
  # Split the name-value pairs
  @pairs = split(/&/, $buffer);
}

foreach $pair (@pairs) {
  local($name, $value) = split(/=/, $pair);
  $FORM{$name} = $value;
}

my $config = LoadFile('config.yaml');

my $org = $FORM{'organism'};
my $fileContents = $FORM{'fileContents'};
$fileContents =~ s/%([A-Fa-f\d]{2})/chr hex $1/eg;

print "Content-Type: text/html\n\n";
# Note there is a newline between
# this header and Data

# Simple HTML code follows

#print "<html> <head>\n";
#print "<title>PANTHER generic mapping</title>";
#print "</head>\n";
#print "<body>\n";
#print "<h1>Hello, world!</h1>\n";
#print "org $org \n";
#print "fileContents $fileContents \n";




my %pthr;
my $panther_classification_directory = $config->{panther_classification_directory};
my $orgFile = "$panther_classification_directory/$org";
open (FH, $orgFile);
while (my $line=<FH>){
    chomp $line;
    #print "processing an organism line $line\n";
    my ($id, $pthr)=split(/\t/, $line);
    $pthr{$id}=$pthr;
}
close (FH);
#print "finished reading org file\n";
my $count1;
my $count2;

my @linesArray = split /\n/, $fileContents;
foreach $line (@linesArray) {
    #print "processing a line $line\n";
    $line=~s/\r//g;
    #chomp $line;
    my ($id, @rest)=split(/\t/, $line);
    my $foo = join("\t", @rest);
    if (defined $pthr{$id}){
	$count1++;
	my $pthr=$pthr{$id};

	print "$id\t$pthr\t$foo\n";
    }else{
        $count2++;
        print "$id\tNOHIT\t$foo\n";
    }
}



#print "</body> </html>\n";
