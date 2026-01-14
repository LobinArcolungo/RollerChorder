import urllib.request
import sys

def parseChords(chords):
    chords=chords.replace(";","")
    chords=chords.replace("&quot","")
    chords=chords.replace(":","")
    chords=chords.replace("\\\\","\\")
    chords=chords.replace("\\n","\n")
    chords=chords.replace("\\r","")
    chords=chords.replace("[tab]","\t")
    chords=chords.replace("[/tab]","\t")
    chords=chords.replace("\\'","\'")
    
    chords=chords.replace("&agrave","i")
    chords=chords.replace("&egrave","i")
    chords=chords.replace("&igrave","i")
    chords=chords.replace("&ograve","i")
    chords=chords.replace("&ugrave","i")
    return chords

def code_of_site(url):
    weburl = urllib.request.urlopen(url)
    return weburl
def main():
    #print(sys.argv[1])
    if sys.argv[1].startswith("https://tabs.ultimate-guitar.com"):
        #site= "https://tabs.ultimate-guitar.com/tab/misc-cartoons/phineas-and-ferb-hemoglobin-highway-chords-1003555"
        site= sys.argv[1]
        txtfile= code_of_site(site)
        content = txtfile.readlines()

        chords= ((str(content[1094]).split("content&quot"))[1].split("revision_id&quot"))[0]
        chords_parsed=parseChords(chords)
        #removing [ch] and [/ch]
        #chords_parsed=chords_parsed.replace("[ch]","").replace("[/ch]","")
        
        print(chords_parsed)
        #SAVING ON MEMORY
        f =open("chords/"+(site.split('/')[-1])+".txt","w")
        f.write((site.split('/')[-1])+"\n")
        f.write(str(chords_parsed)+"\n")
        f.close()

        
        return chords_parsed
        
    else:
        print("faiure")

main()

