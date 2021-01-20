import re
from tkinter import *



class lexer:

    def __init__(self,tokenlist = []):
        self.tokenlist = tokenlist
        

    def cutOneLineTokens(self,string):
    

        while (string != ""): #while string is not empty

            result = re.match(r'^if|^else|^int|^float', string) #keywords to be matched
            if (result != None): #keyword was not found
                tuple1 = ("keyword",result.group()) 
                self.tokenlist.append(tuple1) #add tuple to token list
                string = string.replace(string[:int(result.end())], '', 1) #move to next string
                string = string.strip() #remove any whitespaces before or after string


            string = string.strip()
            result = re.match(r'^[A-Za-z]+', string)  
            if (result != None):
                result = re.match(r'[A-Za-z0-9]+', string)
                tuple1 = ("identifier",result.group())
                self.tokenlist.append(tuple1)
                string = string.replace(string[:int(result.end())], '', 1)
                string = string.strip()


            result = re.match(r'[\(|\)|;|:|"]', string)
            if (result != None):
                tuple1 = ("seperator",result.group())
                value = result.group()
                self.tokenlist.append(tuple1)
                string = string.replace(string[:int(result.end())], '', 1)
                string = string.strip()

                if(value == '"'):
                    result = re.match(r'[A-Za-z\s]+', string)
                    if (result != None):
                        tuple1 = ("str_literal",result.group())
                        self.tokenlist.append(tuple1)
                        string = string.replace(string[:int(result.end())], '', 1)
                        string = string.strip()
                        

            result = re.match(r'^[A-Za-z]+', string)
            if (result != None):
                result = re.match(r'[A-Za-z0-9]+', string)
                tuple1 = ("identifier",result.group())
                self.tokenlist.append(tuple1)
                string = string.replace(string[:int(result.end())], '', 1)
                string = string.strip()

        
            result = re.match(r'[=|+|>|*]', string)
            if (result != None):
                tuple1 = ("operator",result.group())
                self.tokenlist.append(tuple1)
                string = string.replace(string[:int(result.end())], '', 1)
                string = string.strip()

            
            result = re.match(r'\d+\.\d+', string)
            if (result != None):
                tuple1 = ("float_literal",result.group())
                self.tokenlist.append(tuple1)
                string = string.replace(string[:int(result.end())], '', 1)
                string = string.strip()

            
            result = re.match(r'^\d+', string)
            if (result != None):
                tuple1 = ("int_literal",result.group())
                self.tokenlist.append(tuple1)
                string = string.replace(string[:int(result.end())], '', 1)
                string = string.strip()

    

class MyFirstGUI: 

    def __init__(self,root,count = 0,count2 = 0):
        #Master is the default parent object of all widgets.
        self.master = root
        self.master.title("Lexer and Parser for TinyPie")

        self.count = count #line count
        self.count2 = count2 #tuple count
        
        #Widget Labels
        self.label_space = Label(self.master, text="      ") 
        self.label_space.grid(row=0,column=0,sticky=W)
        
        
        self.label = Label(self.master, text="Source Code Input:")
        self.label.grid(row=0,column=1,sticky=W)

        self.label_space1 = Label(self.master, text="       ")
        self.label_space1.grid(row=0,column=2,sticky=W)

        self.label1 = Label(self.master, text="Lexical Analyzed Result:")
        self.label1.grid(row=0,column=3,sticky=W)

        self.label2 = Label(self.master, text="Parser:")
        self.label2.grid(row=0,column=5,sticky=W)

        self.input = Text(self.master, highlightbackground = 'orange' , width = 60)
        self.input.grid(row=1, column=1, sticky =E)

        self.output = Text(self.master, highlightbackground = 'orange', width = 60)
        self.output.grid(row=1, column=3, sticky =E)
        self.output.bind("<Key>", lambda e: "break")

        self.label_space2 = Label(self.master, text="       ")
        self.label_space2.grid(row=0,column=4,sticky=W)

        self.output2 = Text(self.master, highlightbackground = 'orange',width = 60)
        self.output2.grid(row=1, column=5, sticky =E)
        self.output2.bind("<Key>", lambda e: "break")

        self.label_space3 = Label(self.master, text="       ")
        self.label_space3.grid(row=0,column=6,sticky=W)

        self.currline = Label(self.master, text="Current Processing Line: ")
        self.currline.grid(row=2,column=1,sticky=W)

        self.lineoutput = Entry(self.master, width = 10, highlightbackground = 'black' )
        self.lineoutput.grid(row=2,column=1,sticky=E)
        self.lineoutput.insert(0,self.count)

        self.submitbutton = Button (self.master, text="Next Line", command = self.nextline)
        self.submitbutton.grid(row=3,column=1, sticky=E)

        self.quitbutton = Button (self.master, text="Quit", command = self.master.destroy)
        self.quitbutton.grid(row=3,column=3, sticky=E)

        self.lex = lexer()

    #Accepts token and removes it from the list
    def accept_token(self):
        self.output2.insert(END, "     accept token from the list:"+self.inToken[1])
        self.output2.insert(END,'\n')
        self.inToken=self.lex.tokenlist.pop(0)

    #multiplication check
    def multi(self):
        self.output2.insert(END, "\n----parent node math, finding children nodes:")
        self.output2.insert(END,'\n')
        if(self.inToken[0]=="float_literal"):
            self.output2.insert(END, "child node (internal): float")
            self.output2.insert(END,'\n')
            self.output2.insert(END, "   float has child node (token):"+self.inToken[1])
            self.output2.insert(END,'\n')
            self.accept_token()
        elif (self.inToken[0]=="int_literal"):
            self.output2.insert(END, "child node (internal): int")
            self.output2.insert(END,'\n')
            self.output2.insert(END, "   int has child node (token):"+self.inToken[1])
            self.output2.insert(END,'\n')
            self.accept_token()

            if(self.inToken[1]=="*"):
                self.output2.insert(END, "child node (token):"+self.inToken[1])
                self.output2.insert(END,'\n')
                self.accept_token()

                self.output2.insert(END, "child node (internal): math")
                self.output2.insert(END,'\n')
                self.multi()
            else:
                self.output2.insert(END, "error, you need + after the int in the math")

        else:
            self.output2.insert(END, "error, math expects float or int")


    def math(self):
        self.multi()
        if(self.inToken[1]=="+"):
            self.output2.insert(END, "child node (token):"+self.inToken[1])
            self.output2.insert(END,'\n')
            self.accept_token()
        self.multi()

    
    def exp(self):
        self.output2.insert(END, "\n#######Parse tree for line " + str(self.count) + "#######\n")
        self.output2.insert(END, "\n----parent node exp, finding children nodes:")
        self.output2.insert(END,'\n')

        typeT,token=self.inToken
    
        if(typeT=="keyword"):
            self.output2.insert(END, "child node (internal): keyword")
            self.output2.insert(END,'\n')
            self.output2.insert(END, "   identifier has child node (token):"+token)
            self.output2.insert(END,'\n')
            self.accept_token()
        else:
            self.output2.insert(END, "expect keyword as the first element of the expression!\n")
            return
    
        if(self.inToken[0]=="identifier"):
            self.output2.insert(END, "child node (internal): identifier")
            self.output2.insert(END,'\n')
            self.output2.insert(END, "   identifier has child node (token):"+self.inToken[1])
            self.output2.insert(END,'\n')
            self.accept_token()
        else:
            self.output2.insert(END, "expect identifier as the first element of the expression!\n")
            return

        if(self.inToken[1]=="="):
            self.output2.insert(END, "child node (token):"+self.inToken[1])
            self.output2.insert(END,'\n')
            self.accept_token()
        else:
            self.output2.insert(END, "expect = as the second element of the expression!")
            return

        self.output2.insert(END, "Child node (internal): math")
        self.math()


    def comparison_exp(self):

        self.output2.insert(END, "\n----parent node comparison_exp, finding children nodes:\n")
    
        if(self.inToken[0]=="identifier"):
            self.output2.insert(END, "child node (internal): identifier\n")
            self.output2.insert(END, "   identifier has child node (token):"+self.inToken[1]+"\n")
            self.accept_token()

        else:
            self.output2.insert(END, "expect identifier as the third element of the expression!\n")
            return

        if(self.inToken[0]=="operator"):
            self.output2.insert(END, "child node (internal): operator\n")
            self.output2.insert(END, "   operator has child node (token):"+self.inToken[1]+"\n")
            self.accept_token()

        else:
            self.output2.insert(END, "expect operator as the fourth element of the expression!\n")
            return

        if(self.inToken[0]=="identifier"):
            self.output2.insert(END, "child node (internal): identifier\n")
            self.output2.insert(END, "   identifier has child node (token):"+self.inToken[1]+"\n")
            self.accept_token()

        else:
            self.output2.insert(END, "expect identifier as the fifth element of the expression!\n")
            return

    

    def if_exp(self):

        self.output2.insert(END, "\n#######Parse tree for line " + str(self.count) + "#######\n")

        self.output2.insert(END, "\n----parent node if_exp, finding children nodes:\n")
        
        typeT,token=self.inToken
    
        if(typeT=="keyword" and token=="if"):
            self.output2.insert(END, "child node (internal): keyword\n")
            self.output2.insert(END, "   keyword has child node (token):"+token + "\n")
            self.accept_token()
        else:
            self.output2.insert(END, "expect keyword as the first element of the expression!\n")
            return
    
        if(self.inToken[1]=="("):
            self.output2.insert(END, "child node (internal): seperator\n")
            self.output2.insert(END, "   seperator has child node (token):"+self.inToken[1]+"\n")
            self.accept_token()
        else:
            self.output2.insert(END, "expect seperator as the second element of the expression!\n")
            return

        self.comparison_exp()

        self.output2.insert(END, "\n----parent node if_exp, finding children nodes:\n")

        if(self.inToken[1]==")"):
            self.output2.insert(END, "child node (token):"+self.inToken[1]+"\n")
            self.accept_token()
        else:
            self.output2.insert(END, "expect ) as the sixth element of the expression!\n")
            return

        if(self.inToken[1]==":"):

            self.output2.insert(END, "child node (token):"+self.inToken[1])
            self.output2.insert(END, "\nparse tree building success!")
            return

        else:
            self.output2.insert(END, "expect : as the seventh element of the expression!\n")
            return

    def print_exp(self):

        self.output2.insert(END, "\n\n#######Parse tree for line " + str(self.count) + "#######\n")

        self.output2.insert(END, "\n\n----parent node print_exp, finding children nodes:\n")
        
        typeT,token=self.inToken
    
        if(typeT=="identifier" and token=="print"):
            self.output2.insert(END, "child node (internal): identifier\n")
            self.output2.insert(END, "   identifier has child node (token):"+token + "\n")
            self.accept_token()
        else:
            self.output2.insert(END, "expect identifier as the first element of the expression!\n")
            return

        if(self.inToken[1]=="("):
            self.output2.insert(END, "child node (internal): seperator\n")
            self.output2.insert(END, "   seperator has child node (token):"+ self.inToken[1] + "\n")
            self.accept_token()
        else:
            self.output2.insert(END, "expect seperator as the first element of the expression!\n")
            return

        if(self.inToken[1]=='"'):
            self.output2.insert(END, "child node (internal): seperator\n")
            self.output2.insert(END, "   seperator has child node (token):"+ self.inToken[1] + "\n")
            self.accept_token()
        else:
            self.output2.insert(END, "expect seperator as the first element of the expression!\n")
            return

        if(self.inToken[0]=="str_literal"):
            self.output2.insert(END, "child node (internal): str_literal\n")
            self.output2.insert(END, "   str_literal has child node (token):"+ self.inToken[1] + "\n")
            self.accept_token()
        else:
            self.output2.insert(END, "expect str_literal as the first element of the expression!\n")
            return

        
        if(self.inToken[1]=='"'):
            self.output2.insert(END, "child node (internal): seperator\n")
            self.output2.insert(END, "   seperator has child node (token):"+ self.inToken[1] + "\n")
            self.accept_token()
        else:
            self.output2.insert(END, "expect seperator as the first element of the expression!\n")
            return

        if(self.inToken[1]==")"):
            self.output2.insert(END, "child node (internal): seperator\n")
            self.output2.insert(END, "   seperator has child node (token):"+ self.inToken[1] + "\n")
            self.accept_token()
        else:
            self.output2.insert(END, "expect seperator as the first element of the expression!\n")
            return

        if(self.inToken[1]==";"):
            self.output2.insert(END, "child node (token):"+self.inToken[1])
            self.output2.insert(END, "\nparse tree building success!\n")
            return
            

        else:
            self.output2.insert(END, "expect seperator as the first element of the expression!\n")
            return


        
    def parser(self):
        self.inToken=self.lex.tokenlist.pop(0)
        if(self.count==1 or self.count==2):
            self.exp()
            if(self.inToken[1]==";"):
                self.output2.insert(END, "child node (token):"+self.inToken[1])
                self.output2.insert(END, "\nparse tree building success!\n")
                return
        if(self.count==3):
            self.if_exp()

        if(self.count==4):
            self.print_exp()


    
    def nextline(self):        
        text = self.input.get('1.0', 'end').splitlines()
        self.lex.cutOneLineTokens(text[self.count2])
        if(text[self.count2]!=""):
            for item in self.lex.tokenlist:
                self.output.insert(END,'<' + str(item[0]) + ', ' + str(item[1]) + '>')
                self.output.insert(END,'\n')
           
            
            self.lineoutput.delete(0,'end')
            self.count+=1
            self.lineoutput.insert(0,self.count)
            self.parser()
        
        elif(text[self.count2]==""):
            self.output.insert(END,'\n')
            self.lex.tokenlist = []
            self.count2+=1
            self.nextline()

        self.output.insert(END,'\n')
        self.lex.tokenlist = []
        self.count2+=1
        


        
    
        









if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = MyFirstGUI(myTkRoot)
    myTkRoot.mainloop()
