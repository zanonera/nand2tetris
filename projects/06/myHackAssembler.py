from itertools import dropwhile
import sys, getopt, os

def rm_inline_comment(s):
    """ function to remove all the
        double slash inline comment
    """
    # remove all inline double slash (//) comment
    s = s.split('//')
    s = s[0].rstrip()
    s+="\n"
    return s

def rm_space(s):
    """ function to remove all the leading
        white spaces of a line
    """
    # remove all the leading whitespace
    return s.lstrip() 

def is_comment(s):
    """ function to check if a line
         starts with some character.
         Here // for comment
    """
    # return true if a line starts with //
    return s.startswith('//')

def is_space(s):
    """ function to check if a line
         is only white spaces
    """
    # return true if a line is all in whitespace
    return s.isspace() 

def is_address(s):
    """ function to check if a is a A
        instruction
    """
    # return true if a line starts with @
    return s.startswith('@') 
    
def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hvi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('For help use "main.py -h"')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('Hack language assembler - Nand2Tetris Project')
         print('Uses the following syntax to assemble your code:')
         print('# main.py -i <inputfile.asm>')
         print('or')
         print('# main.py -i <inputfile.asm> -o <outputfile.hack>')
         sys.exit()
      elif opt == '-v':
         print('v0.1 - initial work')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
         #If you don't specify the output name it will use the input name and change the file format
         name=os.path.splitext(inputfile)
         outputfile=name[0]+".hack"
         print('Assembled file in:',outputfile)
      elif opt in ("-o", "--ofile"):
         # Uses the name specified in the -o argument
         outputfile = arg
      
   if outputfile:
      fileOut=open(outputfile,"w+")
   
   # Ignore the comments with double slash and whitespace lines
   linha = 0
   if inputfile:
      with open(inputfile,'r') as fileIn:
         for curline in fileIn:
            linha += 1                             ##takes care of the current line count. to translate labels
            curline = rm_space(curline)            ##remove leading white space at current line
            curline = rm_inline_comment(curline)   ##remove in line comments at current line
            if is_comment(curline):
               continue
            elif is_space(curline):
               continue   
            elif is_address(curline):
               decimal=int(curline.strip('@'))
               fileOut.write('0'+bin(decimal)[2:].zfill(15)+'\n')
            else:
               fileOut.write(curline)
      fileIn.close()
      fileOut.close()
   else:
      print("You should specify at least a input file, like:")
      print('# main.py -i <inputfile.asm>')
     
if __name__ == "__main__":
   main(sys.argv[1:])