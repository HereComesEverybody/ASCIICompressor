""" This class compresses an ASCII image by taking advantage of information redundancy
    in the form of frequently-repeating sequences of the same character. """

class ASCIICompressor():

    def __init__(self):
        pass

    def _getCharAndCount(self,string):
        """ Helper function that finds the number of repeats for the first character in
            the string and then returns the first index that holds a different character.
            The return signature is a 3-tuple containing the character that is repeated,
            the number of repeats, and the index immediately after the last repeat.  """

        char,i,count = string[0],1,1
        while i < len(string) and string[i] == char:
            count += 1
            i += 1
        return char,str(count),i

    def _compressCounts(self,counts):
        """ I realized that I could improve the algorithm by compressing redundant sequences of 1s
            in the run-counts (I already represent 1s as empty strings). Thus 2,,,,7 could be represented
            as 2,o3,7, where o3 signifies a sequence of 3 ones. I could have done this with other numbers
            as well (for example, choosing t3 two represent 2,2,2),but I figured that I should keep things
            simple, and that this sufficed for proof of concept.  """
        res = []
        while counts != []:
            # '' means a 1
            if counts[0] == '':
                _,reps,next = self._getCharAndCount(counts)
                # it's only worth it for more than two repetitions
                if int(reps) > 2:
                    res.append('o'+reps)
                else:
                    # otherwise, just keep the original
                    for i in range(int(reps)):
                        res.append('')
                counts = counts[next:]
            else:
                res.append(counts[0])
                counts = counts[1:]
        return res

    def _decompressCounts(self,encoded_counts):
        """ Decompress the counts (i.e. o3 becomes 1,1,1 and '' becomes 1 """
        res = []
        for e in encoded_counts:
            if 'o' in e:
                reps = int(e[1:])
                for i in range(reps):
                    res.append('1')
            elif e == '':
                res.append('1')
            else:
                res.append(e)
        return res


    def encodeImage(self,file_name):
        """ Returns a run-length encoded compressed string representation of an ASCII file
            specified by 'file_name.' The format of the compressed file consists of the number
            of character runs found in the file on the first line (for example, '@@@@' would
            be counted as one character run), then the characters found in each run, then
            finally the corresponding count of each character at the end of the file. Decoupling
            each character from its count per run allows us to handle numerical characters in
            the ASCII file.  """

        image = open(file_name).read()

        # Initialize our character and count segments
        encoded_chars,encoded_counts = '',[]

        # Initialize the number of character runs to 0 """
        char_run_count = 0

        while image != '':

            # Get a character, its number of repeats, and the index at which it stops repeating
            char,count,next = self._getCharAndCount(image)

            # if the count is one, it makes more sense to encode it as the empty string, since otherwise
            # we would be taking up significantly more space than the original. We're still taking up
            # more space, but less so.
            if count == '1':
                count = ''
            char_run_count += 1

            # We do not need to look at portions of the image that we have already processed, so
            # we start again from 'next'
            image = image[next:]

            # Add this data to our encoding
            encoded_chars += char
            encoded_counts.append(count)

        # return the encoded string
        return str(char_run_count)+'\n'+encoded_chars+','.join(self._compressCounts(encoded_counts))

    def decodeImage(self,file_name):
        """ Returns a decoded string representation of a compressed file. This
            should yield a lossless restoration of the original data.  """

        lines = open(file_name).readlines()

        # Get the number of character runs (located on the first line).
        char_run_count = int(lines[0].strip())

        # Get the rest of the encoded data.
        encoded = ''.join(lines[1:])

        decoded = ''

        # Get each character and its corresponding count.
        chars,counts = encoded[:char_run_count],self._decompressCounts(encoded[char_run_count:].split(','))

        # Append 'count' number of each 'char' to the decoded string.
        for char,count in zip(chars,counts):
            if count == '':
                count = '1'
            decoded += char*int(count)

        # Return the decoded string
        return decoded

    def encodeAndWrite(self,in_name,out_name=None):
        """ Encode an ASCII file and output it to a new file.
            If no output name is provided, the output will be
            written to <input name without extension>_compressed.txt.  """
        if not out_name:
            out_name = in_name.split('.txt')[0]+'_compressed.txt'
        open(out_name,'w').write(self.encodeImage(in_name))

    def decodeAndWrite(self,in_name,out_name=None):
        """ Decodes a compressed ASCII file and output it to a new file.
            If no output name is provided, the output will be written
            to <input name without extension>_decompressed.txt.  """

        if not out_name:
            out_name = in_name.split('.txt')[0]+'_decompressed.txt'
        open(out_name,'w').write(self.decodeImage(in_name))