OPTAB=[["ADD","18","3"],["ADDF","58","3"],["ADDR","90","2"],["AND","40","3"],["CLEAR","B4","2"],["COMP","28","3"],["COMPF","88","3"],      ["COMPR","A0","2"],["DIV","24","3"],["DIVF","64","3"],["DIVR","9C","2"],["FIX","C4","1"],["FLOAT","C0","1"],["HIO","F4","1"],["J","3C","3"],["JEQ","30","3"],["JGT","34","3"],["JLT","38","3"],["JSUB","48","3"],["LDA","00","3"],["LDB","68","3"],["LDCH","50","3"],["LDF","70","3"],["LDL","08","3"],["LDS","6C","3"],["LDT","74","3"],["LDX","04","3"],["LPS","D0","3"],["MUL","20","3"],["MULF","60","3"],["MULR","98","2"],
["NORM","C8","1"],["OR","44","3"],["RD","D8","3"],["RMO","AC","2"],["RSUB","4C","3"],["SHIFTL","A4","2"],["SHIFTR","A8","2"],["SIO","F0","1"],["SSK","EC","3"],["STA","0C","3"],["STB","78","3"],["STCH","54","3"],["STF","80","3"],["STI","D4","3"],["STL","14","3"],["STS","7C","3"],
["STSW","E8","3"],["STT","84","3"],["STX","10","3"],["SUB","1C","3"],["SUBF","5C","3"],["SVC","B0","2"],["SUBR","94","2"],["TD","E0","3"],
["TIO","F8","1"],["TIX","2C","3"],["TIXR","B8","2"],["WD","DC","3"]]
def search_optab(opcode):
	global OPTAB
	for i in range(len(OPTAB)):
		if(OPTAB[i][0]==opcode):
			return i
	return -1

def convert(operand):
	hex_val=''
	if(operand[0]=='C'):
		val=operand[2:len(operand)-1]
		for c in val:
			hex_val+=(str(hex(ord(c))).replace('0x',''))
	elif(operand[0]=='X'):
		hex_val=operand[2:len(operand)-1]
	return hex_val
def init_tr(LOCCTR):
	global TR
	TR='T^'+hex(LOCCTR)[2:].zfill(6)+'^  ^'

def check_fit(OBJ):
	global TR
	if(len(OBJ)+len(TR)-TR.count('^')<=69):
		return True
	else:
		return False	
def write_head():
	global out
	out.append(HEADER)
def write_tr():
	global TR
	global out
	#print('bef',TR)
	sz=len(TR[12:])-TR[12:].count('^')
	
	sz/=2
	hexv=hex(int(sz))[2:].zfill(2)
	
	TR=TR[:9]+hexv+TR[11:]
	#print('after',TR)
	out.append(TR)
def write_e(lines):
	if(lines[2]==''):
		add=0x000000
	else:
		#print(lines[2])
		add=SYMTAB[lines[2]][0].zfill(6)
	End='E^'+add
	out.append(End)
def resolve(loc,new):
	global TR
	global out
	#if(loc=='100c'):
		#print('pk')
	loc=int(loc,16)
	#print(loc)
	fin=0
	j=1
	#if(loc==4108):
			#print('check',out)
	for record in out[1:]:
		nn=''
		start=int(record[2:8],16)
		#print('start',start)
		el=record[12:].split('^')
		
		
		while( '' in el):
			el.remove('')
		#print(el)
		#print(el)
		for i in range(len(el)) :
			#print('start',hex(start),'loc',hex(loc))
			#print('ipahah',hex(loc))
			
			if(start==loc):
				
				newb=int(el[i],16)+int(new,16)
				#print('vvvv',hex(new))
				
					
				el[i]=hex(newb)[2:].zfill(6)
				#if(hex(loc)=='100c'):
					#print('hhh',el[i])
				fin=1
				#print('here',el)
				break
			start+=int(len(el[i])/2)
		
			
		if(fin==1):
		
			for k in record[:12]:
				nn+=k
			for k in el:
				nn+=k+'^'
			out[j]=nn
			#print(out[j])
			break
		j+=1
	if( fin==0):
		#print('err',hex(loc))
		start=int(TR[2:8],16)
		el=TR[12:].split('^')
		for i in range(len( el)):
			if(start==loc):
				el[i]=hex(int(el[i],16)+int(new,16))[2:].zfill(6)
				break
				
			start+=int(len(el[i])/2)
		nn=''
		nn+=TR[:12]
		for k in el:
			nn+=k+'^'
		TR=nn

			
def append(obj):
	global TR
	#print("bef",TR)
	if(obj!=''):
		TR+=obj+'^'
	#print("af",TR)		
		
		
			
	 
SYMTAB={}
out=[]
TR=''
HEADER='H^'
start_addr='000000'
LOCCTR=int('000000',16)
source=open('source3.asm')
line=source.readline().rstrip()
lineno=0
done=0
while(line!=''):
	OBJ=''
	lines=line.split('\t')
	#print(lines)
	if(lines[0]=='.'):
		line=source.readline().rstrip()
		lineno+=1
		continue
		
			
	if(len(lines)>1 and lines[1]=='START'):
		if(len(lines)>2):
			start_addr=lines[2].zfill(6)
	if(lineno==0):
		#done=0
		LOCCTR=int(start_addr,16)
		HEADER='H^'+lines[0]+'^'+start_addr+'^  '
		write_head()
		init_tr(LOCCTR)

	if(lines[0]!='.'):
		if(lines[0]!=''):#label present
			if(lines[0] in SYMTAB.keys()):
				if(SYMTAB[lines[0]][0] ==-1):
					SYMTAB[lines[0]][0]=hex(LOCCTR)[2:]
					#if(lines[0]=='ENDFIL'):
						#print('here')
						#print('sssss',SYMTAB[lines[0]][1:])
					for res in SYMTAB[lines[0]][1:]:
						#if(lines[0]=='ENDFIL'):
							#print('lllllll',res)
						resolve(res,hex(LOCCTR))#update refreences
						#print(hex(LOCCTR))
					#remove linked list
					#temp=SYMTAB[lines[0]][0]
					#SYMTAB[lines[0]]=[-1]
					#SYMTAB[lines[0]].append(temp)
					
			else:
				SYMTAB[lines[0]]=[hex(LOCCTR)[2:]]
			#print(SYMTAB)
		
		
		po=search_optab(lines[1])
		if(po!=-1):
			done=0
			operand_ad=''
			if(len(lines)>2):#consider rsub
				if(',' in lines[2]):#index present
					comm=lines[2].split(',')
					#print('comm',comm)
					if(comm[0] in SYMTAB.keys()):
						if(SYMTAB[comm[0]][0] !=-1):
							operand_ad=SYMTAB[comm[0]][0].zfill(3)
						else:
							operand_ad='000'
							SYMTAB[comm[0]].append(hex(LOCCTR)[2:].zfill(3))
							#print(SYMTAB)
					else:
						SYMTAB[comm[0]]=[-1,hex(LOCCTR)[2:].zfill(3)]
						operand_ad='000'
					bina=bin(int(operand_ad,16))[2:]
					bina='1'+bina
					operand_ad=hex(int(bina,2))[2:].zfill(4)
				else:#not index
					if(lines[2] in SYMTAB.keys()):
						if(SYMTAB[lines[2]][0] !=-1):
							#print(SYMTAB)
							operand_ad=SYMTAB[lines[2]][0].zfill(3)
						else:
							operand_ad='000'
							SYMTAB[lines[2]].append(hex(LOCCTR)[2:].zfill(3))
							#print(SYMTAB)
					else:
						SYMTAB[lines[2]]=[-1,hex(LOCCTR)[2:].zfill(3)]
						#if(lines[2]=='ENDFIL'):
							#print('here  lll',SYMTAB[lines[2]])
							
						operand_ad='000'
					#print('operand ad:',operand_ad)
					
					bina=bin(int(operand_ad,16))[2:]
					bina='0'+bina
					
					operand_ad=hex(int(bina,2))[2:].zfill(4)
					#print('operand ad:',operand_ad)
			else:#for rsub
				operand_ad='0000'

			OBJ=OPTAB[po][1]+operand_ad
			#print('test',hex(LOCCTR),lines)
			if(check_fit(OBJ)==False):
				#(TR+'\n')
				write_tr()
				init_tr(LOCCTR)
			append(OBJ)
			LOCCTR+=3
			
			
			
		else:#opcode not found
			#print('test',hex(LOCCTR),lines)
			if(lines[1]=='WORD'):
				done=0
				if(check_fit(OBJ)==False):
					#(TR+'\n')
					write_tr()
					init_tr(LOCCTR)
				OBJ=hex(int(lines[2]))[2:].zfill(6)
				append(OBJ)
				LOCCTR+=3
				
			elif(lines[1]=='RESW'):
				LOCCTR+=3*int(lines[2])
				OBJ=''


				
				#print('resw',hex(LOCCTR))
				if(done==0):
					write_tr()
					TR=''
					#print('init',hex(LOCCTR))
					init_tr(LOCCTR)
					done=1
					line=source.readline().rstrip()
					lineno+=1
					continue
				else:
					TR=''
					#print('init',hex(LOCCTR))
					init_tr(LOCCTR)
					done=1
					line=source.readline().rstrip()
					lineno+=1
					continue
					
			elif(lines[1]=='RESB'):
				LOCCTR+=int(lines[2])
				#print('resb init',hex(LOCCTR),lines)
				#print('done',done)
				OBJ=''


				
				if(done==0):
					write_tr()
					TR=''
					#print('init',hex(LOCCTR))
					init_tr(LOCCTR)
					done=1
					line=source.readline().rstrip()
					lineno+=1
					continue
				else:
					TR=''
					#print('init',hex(LOCCTR))
					init_tr(LOCCTR)
					done=1
					line=source.readline().rstrip()
					lineno+=1
					continue

			elif(lines[1]=='BYTE'):
				done=0
				OBJ=convert(lines[2])
				if(check_fit(OBJ)==False):
					#(TR+'\n')
					write_tr()
					init_tr(LOCCTR)
				append(OBJ)
				LOCCTR+=int(len(OBJ)/2)
		#print(line+'\n',hex(LOCCTR),':',OBJ+'\n')
		#if(check_fit(OBJ)==False):
			#(TR+'\n')
			#write_tr()
			#init_tr(LOCCTR)
		#append(OBJ)
		
		#continue
		if(lines[1]=='END'):
			write_tr()
			write_e(lines)
		
		line=source.readline().rstrip()
		lineno+=1
for rec in out:
	print(rec+'\n')

#print(SYMTAB)
			
				
				
				
				
					
		
					
						
			
			
	
		
		
		
	
