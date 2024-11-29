import socket
import re

def get_open_ports(target, port_range, verbose = False):
    #print(f"host: {target} {port_range} {verbose}")
    ip = ""
    open_ports = []
    
    try:
        ip = socket.gethostbyname(target)
        for port in range(port_range[0], port_range[1]+1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)

            result = s.connect_ex((ip,port))
            if result == 0:
                open_ports.append(port)
            s.close()
    except KeyboardInterrupt:
        return "Exiting Program!!!"
    except socket.gaierror:
        regex = re.search("[a-zA-Z]", target)
        if regex:
            return "Error: Invalid hostname"
        return "Error: Invalid IP address"
    except socket.error:
        return "Error: Invalid IP address"
    host = None
    try:
        host = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        host = None
    final_string = "Open ports for "
    if host == None:
        final_string += f"{ip}"
    else:
        final_string += f"{host} ({ip})"
    final_string += "\n"
    if verbose:
        header = "PORT     SERVICE\n"
        body = ""
        body_format = " " * (9-len(str(port)))
        for port in open_ports:
            body += f"{port}{body_format}{socket.getservbyport(port)}"
            #body += "{p}".format(p=port) + " "*(9-len(str(port))) + "{sn}".format(sn=socket.getservbyport(port))
            #print(body)
            if port != open_ports[len(open_ports)-1]:
                body += "\n"
        return final_string + header + body
    return(open_ports)
