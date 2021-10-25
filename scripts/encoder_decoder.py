def guess_seq_len(seq,patterns):
    max_len = len(seq)/2
    for x in range(2,max_len+1):
        aux = x
        for y in range(0,len(seq)-(aux-1)):
            if seq[y:aux] == seq[y+x:aux+x] or seq[y:aux] in patterns:
                if seq[y:aux] in patterns:
                    patterns[seq[y:aux]] += 1
                else:
                    patterns[seq[y:aux]] = 1                        
                    
            aux += 1
            
            
def change_pattern(pattern):
    res = ''
    pattern = list(pattern)
    for i in pattern:
        res += i
        if pattern.index(i) < len(pattern)-1:
            res += ','
            
    return res
    
            
def encode_seq(seq,patterns):
    smallest = max(patterns,key=patterns.get)
    l = len(smallest)
    
    index = seq.find(smallest)
    
    i = seq.find(smallest)
    aux = i+l
    patterns[smallest] -= 1
    
    sum = 1

    while seq[i:aux] == seq[i+l:aux+l]:
        i += l
        aux += l
        patterns[smallest] -= 1
        sum += 1
        
    smallest = change_pattern(smallest)
    pattern = "["+str(sum)+"x("+str(smallest)+")]"
    newseq = seq[:index]+pattern+seq[aux:]
    
    return newseq
    
    
def decode_seq(seq, mult=1):
    iteration = 'out'
    newseq = ''
    
    for c in seq:
        if c == '[' and iteration == 'out':
            iteration = 'mult'
            sum = 0
        
        elif iteration == 'mult' and c != 'x':
            sum += int(c)
        
        elif c == 'x':
            iteration = 'pattern'
            pattern = ''
        
        elif iteration == 'pattern' and c != ']':
            if c != '(' and c != ',' and c != ')':
                pattern += c
            
        elif c == ']' and iteration == 'pattern':
            newseq += int(sum*mult)*pattern
            iteration = 'out'
        
        else:
            newseq += c
            
    return newseq


def main(seq):
	#ex: seq = "010111010"
	print seq
	patterns = {}
	guess_seq_len(seq,patterns)
	print patterns
	seq = encode_seq(seq,patterns)
	while patterns != {}:
		print seq
		patterns = {}
		guess_seq_len(seq,patterns)
		print patterns
		if patterns != {}:
			seq = encode_seq(seq,patterns)
        
        

	print decode_seq(seq,1.5)
