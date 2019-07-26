#! /usr/local/bin/perl

#####
#####
##  
##   This script is to map the id in your gene list to PANTHER classificaiton.
##
##   Inputs:
##     -i  The PANTHER classification file for the genome of your interest
##     -g  Your gene list (tab-deliminated simple text file with the UniProt ID
##          in the first column) 
##
#####
#####

# get command-line arguments
use Getopt::Std;
getopts('o:i:g:e:vVh') || &usage();
&usage() if ($opt_h);         # -h for help
$outDir = $opt_o if ($opt_o);    # -o for (o)utput directory
$inFile = $opt_i if ($opt_i);     # -i for the input pthr mapping file
$geneList = $opt_g if ($opt_g);   # -g for the gene list
$errFile = $opt_e if ($opt_e);    # -e for (e)rror file (redirect STDERR)
$verbose = 1 if ($opt_v);         # -v for (v)erbose (debug info to STDERR)
$verbose = 2 if ($opt_V);         # -V for (V)ery verbose (debug info STDERR)

my %pthr;
open (FH, $inFile);
while (my $line=<FH>){
    chomp $line;
    my ($id, $pthr)=split(/\t/, $line);
    $pthr{$id}=$pthr;
}
close (FH);

my $count1;
my $count2;
open (GL, $geneList);
while (my $line=<GL>){
    $line=~s/\r//g;
    chomp $line;
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
close (GL);

print STDERR "$count1 IDs can be mapped.\n";
print STDERR "$count2 IDs are not mapped.\n";
