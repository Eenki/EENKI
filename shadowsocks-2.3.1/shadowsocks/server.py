#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
import signal
import utils
import encrypt
import eventloop
import tcprelay
import udprelay
import asyncdns


def main():
    utils.check_python()

    config = utils.get_config(False)

    utils.print_decs()

    if config['port_password']:
        if config['password']:
            logging.warn('warning: port_password should not be used with '
                         'server_port and password. server_port and password '
                         'will be ignored')
    else:
        config['port_password'] = {}
        server_port = config['server_port']
        if type(server_port) == list:
            for a_server_port in server_port:
                config['port_password'][a_server_port] = config['password']
        else:
            config['port_password'][str(server_port)] = config['password']

    encrypt.init_table(config['password'], config['method'])
    tcp_servers = []
    udp_servers = []
    dns_resolver = asyncdns.DNSResolver()
    for port, password in config['port_password'].items():
        a_config = config.copy()
        a_config['server_port'] = int(port)
        a_config['password'] = password
        logging.info("starting server at %s:%d" %
                     (a_config['server'], int(port)))
        tcp_servers.append(tcprelay.TCPRelay(a_config, dns_resolver, False))
        udp_servers.append(udprelay.UDPRelay(a_config, dns_resolver, False))

    def run_server():
        def child_handler(signum, _):
            logging.warn('received SIGQUIT, doing graceful shutting down..')
            map(lambda s: s.close(next_tick=True), tcp_servers + udp_servers)
        signal.signal(getattr(signal, 'SIGQUIT', signal.SIGTERM),
                      child_handler)
        try:
            loop = eventloop.EventLoop()
            dns_resolver.add_to_loop(loop)
            map(lambda s: s.add_to_loop(loop), tcp_servers + udp_servers)
            loop.run()
        except (KeyboardInterrupt, IOError, OSError) as e:
            logging.error(e)
            if config['verbose']:
                import traceback
                traceback.print_exc()
            os._exit(1)

    if int(config['workers']) > 1:
        if os.name == 'posix':
            children = []
            is_child = False
            for i in xrange(0, int(config['workers'])):
                r = os.fork()
                if r == 0:
                    logging.info('worker started')
                    is_child = True
                    run_server()
                    break
                else:
                    children.append(r)
            if not is_child:
                def handler(signum, _):
                    for pid in children:
                        try:
                            os.kill(pid, signum)
                        except OSError:  # child may already exited
                            pass
                    sys.exit()
                signal.signal(signal.SIGTERM, handler)
                signal.signal(signal.SIGQUIT, handler)

                # master
                for a_tcp_server in tcp_servers:
                    a_tcp_server.close()
                for a_udp_server in udp_servers:
                    a_udp_server.close()
                dns_resolver.close()

                for child in children:
                    os.waitpid(child, 0)
        else:
            logging.warn('worker is only available on Unix/Linux')
            run_server()
    else:
        run_server()


if __name__ == '__main__':
    main()
