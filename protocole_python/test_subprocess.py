import subprocess


process = subprocess.Popen(['ping', 'geekflare.com'], stdout=subprocess.PIPE, text=True)
while True:
    output = process.stdout.readline()
    if output:
        #type(output.strip())
    	print(type(output.strip()))
    #result = process.poll()
    