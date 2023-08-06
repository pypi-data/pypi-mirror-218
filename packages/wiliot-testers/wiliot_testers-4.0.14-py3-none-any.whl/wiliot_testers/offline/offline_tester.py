"""
  Copyright (c) 2016- 2023, Wiliot Ltd. All rights reserved.

  Redistribution and use of the Software in source and binary forms, with or without modification,
   are permitted provided that the following conditions are met:

     1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

     2. Redistributions in binary form, except as used in conjunction with
     Wiliot's Pixel in a product or a Software update for such product, must reproduce
     the above copyright notice, this list of conditions and the following disclaimer in
     the documentation and/or other materials provided with the distribution.

     3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
     may be used to endorse or promote products or services derived from this Software,
     without specific prior written permission.

     4. This Software, with or without modification, must only be used in conjunction
     with Wiliot's Pixel or with Wiliot's cloud service.

     5. If any Software is provided in binary form under this license, you must not
     do any of the following:
     (a) modify, adapt, translate, or create a derivative work of the Software; or
     (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
     discover the source code or non-literal aspects (such as the underlying structure,
     sequence, organization, ideas, or algorithms) of the Software.

     6. If you create a derivative work and/or improvement of any Software, you hereby
     irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
     royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
     right and license to reproduce, use, make, have made, import, distribute, sell,
     offer for sale, create derivative works of, modify, translate, publicly perform
     and display, and otherwise commercially exploit such derivative works and improvements
     (as applicable) in conjunction with Wiliot's products and services.

     7. You represent and warrant that you are not a resident of (and will not use the
     Software in) a country that the U.S. government has embargoed for use of the Software,
     nor are you named on the U.S. Treasury Department’s list of Specially Designated
     Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
     You must not transfer, export, re-export, import, re-import or divert the Software
     in violation of any export or re-export control laws and regulations (such as the
     United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
     and use restrictions, all as then in effect

   THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
   OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
   WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
   QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
   IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
   ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
   OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
   FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
   (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
   (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
   (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
   (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
"""
import csv
import os.path
from datetime import datetime
import argparse
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
from wiliot_testers.test_equipment import BarcodeScanner
from numpy import mean
from wiliot_testers.wiliot_tester_tag_test import *
from wiliot_testers.wiliot_tester_log import *
from wiliot_testers.tester_utils import *
from wiliot_testers.utils.upload_to_cloud_api import *
from wiliot_testers.offline.offline_utils import *
from wiliot_core import WiliotDir, check_user_config_is_ok, csv_to_dict, InlayTypes, DualGWMode, WiliotGateway
from wiliot_testers.utils.get_version import get_version
from wiliot_core import WiliotGateway, DualGWMode
from appdirs import user_data_dir
from queue import Queue
import socket

# a global variable which will be in the log_file name that says the R2R code version
n_tag_counter_position = 4  # 4 characters on the esternal id indicate tag counter in the reel
R2R_code_version = '13'
# running parameters
tested = 0
passed = 0
responded = 0
under_threshold = 0
missing_labels = 0
black_list_size = 0
last_pass_string = 'No tag has passed yet :('

desired_pass_num = 999999999  # this will be set to the desired pass that we want to stop after
desired_tags_num = 999999999  # this will be set to the desired tags that we want to stop after
reel_name = ''
common_run_name = ''
temperature_sensor_enable = False
problem_in_locations_hist = None
fail_bin_list = []
run_start_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
run_start_time_ = datetime.datetime.now()
qr_que_list = []
external_id_for_printer = 999999999
yield_over_time = 0
calculate_interval = 10
calculate_on = 50

MIN_TEST_TIME = 1.5  # seconds
TIME_BTWN_PRINTER_REQUESTS = 0.25  # seconds
PRINTER_SOCKET_TIMEOUT = 1  # seconds

lock_print = threading.Lock()


class QRThread(threading.Thread):
    def __init__(self, events, ports_and_guis, print=False):
        threading.Thread.__init__(self)
        self.events = events
        self.is_print = print
        self.ports_and_guis = ports_and_guis
        self.qr_comport = self.ports_and_guis.Tag_Value['QRcomport']
        self.max_wrong_readouts_in_row = int(self.ports_and_guis.Tag_Value['maxQRWrongTags'])
        self.qr_timeout = str(self.ports_and_guis.Tag_Value['QRtimeout'])

        try:
            if self.is_print:
                self.scanner = BarcodeScanner(com_port='COM{}'.format(self.qr_comport), log_type='LOG', write_to_log=False, timeout=self.qr_timeout, log_name=self.ports_and_guis.my_logger.results_logger.name)
            else:
                self.scanner = BarcodeScanner(com_port='COM{}'.format(self.qr_comport), log_type='LOG', write_to_log=True, timeout=self.qr_timeout, log_name=self.ports_and_guis.my_logger.results_logger.name)

            self.ports_and_guis.my_logger.logger.info('Connected to scanner at port COM{}'.format(self.qr_comport))

        except Exception as e:
            self.ports_and_guis.my_logger.logger.info('No barcode scanner found')
            raise Exception(f'could not connect to bracode scanner {e}')

        self.read_out_attempts = 5
        self.failed_qr_list = []
        self.qr_max_bad_tags = 10
        if 'qr_max_bad_tags' in self.ports_and_guis.Tag_Value:
            try:
                self.qr_max_bad_tags = int(self.ports_and_guis.Tag_Value['qr_max_bad_tags'])
            except Exception as e:
                self.ports_and_guis.my_logger.logger.warning(f'Could not convert the qr_max_bad_tags to number, '
                                                             f'the default value would be {self.qr_max_bad_tags}: {e}')
        self.wrong_readout = 0
        self.wrong_readout_in_row = 0

    def run(self):

        def success_read():
            self.ports_and_guis.my_logger.logger.info("QR code validated successfully")
            self.events.qr_val.set()
            self.events.qr_read_success.set()
            self.success = True
            self.wrong_readout_in_row = 0

        die = False

        while not die:
            time.sleep(0)
            self.events.start_compare.wait(timeout=10)
            if not self.events.start_compare.is_set():
                if self.events.done_to_tag_thread.is_set() or self.events.done_to_r2r_thread.is_set():
                    die = True
                    break
                continue

            if not self.is_print:
                self.events.start_compare.clear()
                self.events.qr_val.clear()
                self.success = False
                for i in range(self.read_out_attempts):
                    self.qr_tag = self.scanner.scan_ext_id()
                    self.ports_and_guis.my_logger.logger.info('Scanned {}'.format(self.qr_tag))
                self.events.qr_val.set()
                self.events.qr_read_success.set()


            else:
                if not self.events.qr_queue.empty():
                    self.events.start_compare.clear()
                    self.events.qr_val.clear()
                    try:
                        self.tag_comparted = self.events.qr_queue.get(block=False, timeout=0.1)
                    except Exception:
                        die = True
                        break
                    self.success = False
                    self.ports_and_guis.my_logger.logger.info('Comparing {}'.format(self.tag_comparted))
                    for i in range(self.read_out_attempts):
                        self.qr_tag = self.scanner.scan_ext_id()
                        self.ports_and_guis.my_logger.logger.info(
                            f'--- SCANNING: expected ex id: {self.tag_comparted["externalID"]}, '
                            f'read ex id: {self.qr_tag[0]} ---')
                        if self.qr_tag[1] is not None:
                            if self.tag_comparted['status'] == 'Pass':
                                if self.tag_comparted['externalID'][-4:] == self.qr_tag[1]:
                                    success_read()
                                    break

                        else:
                            if self.tag_comparted['status'] == 'Fail':
                                success_read()
                                break

                        self.ports_and_guis.my_logger.logger.info(
                            "Scanning failed, trying again attempt {}/{}".format(i, self.read_out_attempts))

                    if not self.success:
                        self.ports_and_guis.my_logger.logger.warning('Scan failed for tag {}'.format(self.tag_comparted))
                        self.wrong_readout += 1
                        self.wrong_readout_in_row += 1
                        if self.wrong_readout < self.qr_max_bad_tags and \
                                self.wrong_readout_in_row < self.max_wrong_readouts_in_row:
                            self.events.qr_val.clear()
                            self.events.qr_read_success.set()

                if self.wrong_readout >= self.qr_max_bad_tags:
                    die = True
                    self.ports_and_guis.my_logger.logger.warning('Maximum bad tags comparing reached')
                    break

                if self.wrong_readout_in_row >= self.max_wrong_readouts_in_row:
                    self.ports_and_guis.my_logger.logger.warning('Maximum bad tags comparing in row reached')
                    die = True
                    break

                if self.events.done_to_tag_thread.is_set() or self.events.done_to_r2r_thread.is_set():
                    die = True
                    break

        if die:
            self.scanner.close_port()
            msg = 'Pausing run because QR comparing went wrong or run end'
            printing_func(msg, 'QRThread', lock_print, logger_type='warning',
                          logger_name=self.ports_and_guis.my_logger.logger.name)
            self.events.done_to_tag_thread.set()
            self.events.stop_to_r2r_thread.set()


class Printer(threading.Thread):
    """
    thread that turns printer on, checks that the print was successful after every tag,

    Parameters:
    @type start_value: int
    @param start_value: first external ID to print on first tag
    @type pass_job_name: str
    @param pass_job_name: the printer pass job name
    @type events: class MainEvents (costume made class that has all of the Events of the program threads)
    @param events: has all of the Events of the program threads
    @type ports_and_guis: class PortsAndGuis (costume made class that has all of the ports and gui inputs for the
                        program threads)
    @param ports_and_guis: has all of the ports and gui inputs for the program threads

    Exceptions:
    @except PrinterNeedsResetException: means that we need to close the program:
            'The printer initialization process has failed in command:...',
            'Printer failed to switch to running mode',
            'The printer over-all-state is Shutdown',
            'The printer over-all-state is Starting up',
            'The printer over-all-state is Shutting down',
            'The printer over-all-state is Offline',
            'reopen_sock() failed'
    @except Exception: operate according to the description:
            'The printer error-state is Warnings present',
            'The printer error-state is Faults present',
            'The printer printed Fail to the previous tag',
            'The printer have not printed on the last tag'

    Events:
        listen/ waits on:
            events.r2r_ready_or_done2tag    => user pressed Stop (end the program)
            events.done_to_printer_thread             => user pressed Stop (end the program) - to avoid deadlock
            events.r2r_ready                => printing was made
            events.was_pass_to_printer      => the last printing was pass
        sets:
            events.printer_error            => the last print was not successful, will cause pause to this run
                                                (and will trigger exception according to the situation)
            events.printer_success          => the last print was successful

    Logging:
        the logging from this thread will be also to logging.debug()
    """

    def __init__(self, start_value, pass_job_name, events, ports_and_guis):
        """
        Initialize Constants
        """
        super(Printer, self).__init__()
        try:
            self.ports_and_guis = ports_and_guis
            self.TCP_BUFFER = self.ports_and_guis.configs_for_printer_values['TCP_BUFFER']
            self.job_name = ''
            self.line_number = ''
            self.sgtin = 'sgtin'
            self.reel_num = 'reel_num'
            self.first_tag_counter = 'tag_number'
            self.pass_counter = 0
            self.fail_counter = 0
            self.printer_response_timeout = 1.5  # time in seconds for printer to answer with updated printing value
            self.timer_is_done = False
            self.exception_queue = Queue()
            self.printing_format = self.ports_and_guis.Tag_Value['printingFormat']
            self.qr_enable = self.ports_and_guis.Tag_Value['QRRead']
            self.roll_sgtin = self.ports_and_guis.Tag_Printing_Value['stringBeforeCounter']
            self.enable_line_selection = self.ports_and_guis.Tag_Printing_Value['enableLineSelection'].lower() == 'yes'
            self.events = events
            self.r2r_ready_or_done2tag_or_done_to_printer_thread = or_event_set(events.r2r_ready_or_done2tag,
                                                                                events.done_to_printer_thread)
            self.start_value = start_value
            self.cur_value = 0
            self.pass_job_name = pass_job_name
            self.fail_job_name = self.ports_and_guis.Tag_Printing_Value['failJobName']
            self.pass_job_num = self.ports_and_guis.Tag_Printing_Value['passJobNum']
            self.fail_job_num = 1


            # open the socket & config the printer
            self.initialization()

        except Exception:
            exception_details = sys.exc_info()
            self.exception_queue.put(exception_details)

    def initialization(self, use_current_value=False):
        """
        Initialize Constants and socket
        @param use_current_value: will indicate that this is not the first initialization at this run
                                    (make the next print to continue from the last printed value)
        """
        try:
            cmds = []
            self.ports_and_guis.open_printer_socket()  # will open and connect the socket
            self.set_printer_to_running()
            # after printer crash - make sure the continue will be from a the old counter
            if use_current_value:
                global external_id_for_printer
                config_start_value = external_id_for_printer
            else:
                config_start_value = self.start_value
            # initialization protocol
            if 'BARCODE' in self.pass_job_name.upper():
                job_fields = [f'reel_num={self.roll_sgtin}T']
            elif 'SGTIN' in self.pass_job_name.upper():
                job_fields = [f'sgtin={self.roll_sgtin[:18]}', f'reel_num={self.roll_sgtin[18:26]}T']
            else:
                printing_func('The print Job Name inserted is not supported at the moment, You will need to press Stop',
                              'PrinterThread', lock_print, logger_type='debug',
                              logger_name=self.ports_and_guis.my_logger.logger.name)
                raise Exception('The print Job Name inserted is not supported at the moment')

            job_fields.append(f'tag_number={config_start_value}')
            job_fields.append('\r\n')
            job_fields_str = '|'.join(job_fields)

            cmds = ['CAF\r\n',
                    'CQI\r\n',
                    f'CLN|{self.fail_job_num}|\r\n',
                    f'CLN|{self.pass_job_num}|\r\n',
                    f'LAS|{self.pass_job_name}|{self.pass_job_num}|' + job_fields_str]
            if self.fail_job_name == self.pass_job_name:
                cmds.append(f'LAS|{self.pass_job_name}|{self.fail_job_num}|' + job_fields_str)
            else:
                cmds.append(f'LAS|{self.fail_job_name}|{self.fail_job_num}|\r\n')

            if self.enable_line_selection:
                cmds.append(self.get_line_selection_cmd(self.fail_job_name))  # select line
            for cmd in cmds:
                value = self.query(cmd)
                time.sleep(0.1)
                # check if the return value is good, if not retry again for 10 times
                counter = 0
                while counter < 10:
                    # 'CQI' fails if the queue is empty
                    if value == 'ERR' and 'CQI' not in cmd:
                        counter += 1
                        time.sleep(0.1)
                        value = self.query(cmd)
                    else:
                        break
                if counter >= 10:
                    self.events.printer_error.set()
                    raise PrinterNeedsResetException('The printer initialization process has failed in command: ' + cmd)
            # get the current counter value
            value = self.query(self.get_state_request())
            if value == 'ERR':
                self.events.printer_error.set()
                raise PrinterNeedsResetException(
                    'The printer initialization process has failed in command: ' + self.get_state_request())
            else:
                parts = [p for p in value.split("|")]
                self.cur_value = int(parts[5])

            if not self.events.printer_error.isSet():
                printing_func('printer thread is ready after initialization',
                              'PrinterThread', lock_print, logger_type='debug',
                              logger_name=self.ports_and_guis.my_logger.logger.name)
                self.events.printer_success.set()
        except Exception:
            exception_details = sys.exc_info()
            self.exception_queue.put(exception_details)

    def set_printer_to_running(self):
        """
        sets the printer to running mode
        Zipher Text Communications Protocol
        printer state machine:
           0 -> 1                      shutdown
           1 -> 4 (automatically)      starting-up
           2 -> 0 (automatically)      shutting-down
           3 -> 2, 4                   running
           4 -> 2, 3                   offline
        @except: PrinterNeedsResetException('Printer failed to switch to running mode')
        @return: None
        """
        res = self.query(self.get_state_request())
        parts = res.split("|")
        if parts[1] == '0':  # (Shut down)
            res = self.query(self.set_state_command('1'))
            if res == 'ACK':
                counter = 0
                while counter < 10:
                    time.sleep(1)
                    res = self.query(self.set_state_command('3'))
                    if res == 'ACK':
                        return
                    counter += 1
        elif parts[1] == '3':  # (Running)
            return
        elif parts[1] == '4':  # (Offline)
            res = self.query(self.set_state_command('3'))
            if res == 'ACK':
                return

        self.events.printer_error.set()
        raise PrinterNeedsResetException('Printer failed to switch to running mode')

    def run(self):
        """
        runs the thread
        """
        global passed
        # this flag will tell the printer to restart its run() (for a case of connectionError)
        do_the_thread_again = True
        while do_the_thread_again:
            do_the_thread_again = False
            time.sleep(0)
            self.ports_and_guis.my_logger.logger.debug('Starting printer inner loop')
            while not self.events.done_to_printer_thread.isSet():
                time.sleep(0)
                try:
                    self.r2r_ready_or_done2tag_or_done_to_printer_thread.wait()
                    if self.events.done_to_printer_thread.isSet() or self.events.done_to_r2r_thread.is_set() or \
                            self.events.done_to_tag_thread.is_set():
                        do_the_thread_again = False
                        break

                    if self.qr_enable != 'Yes':
                        self.ports_and_guis.my_logger.logger.info('Waiting for start compare')
                        self.events.start_compare.wait(timeout=10)  # Wait for QR scan flag
                        if not self.events.start_compare.is_set():
                            if self.events.done_to_tag_thread.is_set() or self.events.done_to_r2r_thread.is_set():
                                do_the_thread_again = False
                                break
                            else:
                                continue
                        else:
                            self.cur_value += 1
                            self.events.start_compare.clear()
                            t_i = datetime.datetime.now()
                            dt = 0.0
                            while dt < MIN_TEST_TIME:
                                try:
                                    self.printer_status()
                                    break
                                except Exception as e:
                                    self.ports_and_guis.my_logger.logger.info(f'got exception from printer, '
                                                                              f'try again ({e})')
                                    dt = (datetime.datetime.now() - t_i).total_seconds()
                                    time.sleep(TIME_BTWN_PRINTER_REQUESTS)
                            if self.enable_line_selection:
                                self.set_printing_type()  # set the printing type for the next tag #TODO need to enable it for QR as well

                except Exception:
                    do_the_thread_again = False
                    exception_details = sys.exc_info()
                    self.exception_queue.put(exception_details)
                    exc_type, exc_obj, exc_trace = exception_details
                    self.events.printer_error.set()  # to avoid deadlocks
                    if isinstance(exc_obj, PrinterNeedsResetException):
                        self.events.stop_to_r2r_thread.set()
                        self.r2r_ready_or_done2tag_or_done_to_printer_thread.wait()
                        break
                    elif isinstance(exc_obj, ConnectionResetError):
                        self.r2r_ready_or_done2tag_or_done_to_printer_thread.wait()
                        try:
                            self.reopen_sock()
                            do_the_thread_again = True
                            self.events.done_to_printer_thread.clear()
                            continue
                        except Exception:
                            exception_details = sys.exc_info()
                            printing_func(
                                'self.reopen_sock() in printer thread failed, will end this run. {}'.format(
                                    format_exception_details(exception_details)),
                                'PrinterThread', lock_print, logger_type='debug',
                                logger_name=self.ports_and_guis.my_logger.logger.name)
                            self.exception_queue.put(exception_details)
                            exc_type, exc_obj, exc_trace = exception_details
                            self.events.printer_error.set()  # to avoid deadlocks
                            if isinstance(exc_obj, PrinterNeedsResetException):
                                self.r2r_ready_or_done2tag_or_done_to_printer_thread.wait()
                                break
                    else:
                        self.events.stop_to_r2r_thread.set()  # to avoid from the run to continue printing in this case

        self.closure()
        printing_func("Exited the while loop of printer thread", 'PrinterThread', lock_print, logger_type='debug',
                      logger_name=self.ports_and_guis.my_logger.logger.name)
        return

    def tag_status_to_job_type(self, tag_status):
        if tag_status.lower() == 'fail':
            job_type = self.fail_job_name
        elif tag_status.lower() == 'pass':
            job_type = self.pass_job_name
        else:
            self.ports_and_guis.my_logger.logger.warning(
                'printing status should be fail or pass, but received "{}" satuts, '
                'please restart the run'.format(tag_status))
            raise PrinterNeedsResetException(
                'printing status should be fail or pass, please check printer and rerun')
        return job_type

    def get_line_selection_cmd(self, job_name):
        if job_name == self.fail_job_name:
            line = self.fail_job_num
        elif job_name == self.pass_job_name:
            line = self.pass_job_num
        else:
            raise Exception(f'for line selection job name must be {self.fail_job_name} or {self.pass_job_name}')

        return 'LSL|' + str(line) + '|\r\n'

    def set_printing_type(self):
        """
        line selection
        @return:
        @rtype:
        """
        try:
            tag_status = self.events.tag_status_queue.get(block=False, timeout=0.2)
            printing_type = self.tag_status_to_job_type(tag_status)
            line_selection_msg = self.get_line_selection_cmd(printing_type)
            rsp = ''
            t_0 = datetime.datetime.now()
            dt = 0
            timeout_ack = 1
            while rsp != 'ACK' and dt < timeout_ack:
                rsp = self.query(line_selection_msg)
                if rsp == 'ACK':
                    return
                dt = (datetime.datetime.now() - t_0).total_seconds()
            self.ports_and_guis.my_logger.logger.warning('Did not get ACK for Line Selection')
            raise PrinterNeedsResetException('Did not get ACK for Line Selection')
        except Empty:
            self.ports_and_guis.my_logger.logger.warning('during printer line selection got exception for empty queue')
            raise PrinterNeedsResetException('Did not get ACK for Line Selection')
        except Exception as e:
            self.ports_and_guis.my_logger.logger.warning('during printer line selection an error occurs: {}'.format(e))
            raise PrinterNeedsResetException('Did not get ACK for Line Selection')

    def printer_status(self):
        """
        checks if the printing value matches the values registered to the logs
        should be called only after self.events.r2r_ready was set
        Exceptions:
            @except Exception('The printer printed Pass to the previous tag'):
                    printer printed pass while it should have been print fail
            @except Exception('The printer printed Fail to the previous tag')
                    printer printed fail while it should have been print pass
            @except Exception('The printer have not printed on the last tag')
                    printer did not print while it should have been
        """
        res = self.query(
            self.get_state_request())  # STS|<overallstate>|<errorstate>|<currentjob>|<batchcount>|<totalcount>
        parts = [p for p in res.split("|")]
        self.ports_and_guis.my_logger.logger.info(
            'Starting comparing value {} with {}'.format(str(self.cur_value), str(parts[5])))
        if parts[1] == '3':
            if parts[2] == '0':
                self.ports_and_guis.my_logger.logger.debug('Printer status is online')
                if int(parts[5]) == self.cur_value:
                    if not self.ports_and_guis.print_test and self.qr_enable != 'Yes':
                        try:
                            expected_printing_type = self.events.qr_queue.get(block=False, timeout=0.2)
                            expected_printing_type = expected_printing_type['status'].lower()
                        except Exception as e:
                            self.ports_and_guis.my_logger.logger.warning(
                                'printing type queue problem, please restart the run ({})'.format(e))
                            expected_printing_type = ''

                        job_type = self.tag_status_to_job_type(expected_printing_type)

                        if parts[3] == job_type:
                            self.events.printer_validation_success.set()
                            self.ports_and_guis.my_logger.logger.debug(
                                'Compare success with type {}'.format(job_type))
                        else:
                            self.events.printer_error.set()
                            raise PrinterNeedsResetException(
                                'The printer type was not right, please check printer and rerun')
                    else:
                        self.events.printer_validation_success.set()
                        self.ports_and_guis.my_logger.logger.debug('Compare success')

                else:
                    self.events.printer_error.set()
                    raise PrinterNeedsResetException(
                        'The printer counter is not synced, please check printer and rerun')
            else:
                if parts[2] == '1':
                    self.events.printer_error.set()
                    raise PrinterNeedsResetException('The printer error-state is Warnings present')
                if parts[2] == '2':
                    self.events.printer_error.set()
                    raise PrinterNeedsResetException('The printer error-state is Faults present')

        else:
            if parts[1] == '0':
                self.events.printer_error.set()
                raise PrinterNeedsResetException('The printer over-all-state is Shutdown')
            if parts[1] == '1':
                self.events.printer_error.set()
                raise PrinterNeedsResetException('The printer over-all-state is Starting up')
            if parts[1] == '2':
                self.events.printer_error.set()
                raise PrinterNeedsResetException('The printer over-all-state is Shutting down')
            if parts[1] == '4':
                self.events.printer_error.set()
                raise PrinterNeedsResetException('The printer over-all-state is Offline')
            if parts[2] == '1':
                self.events.printer_error.set()
                raise PrinterNeedsResetException('The printer error-state is Warnings present')
            if parts[2] == '2':
                self.events.printer_error.set()
                raise PrinterNeedsResetException('The printer error-state is Faults present')

    def end_of_time(self):
        """
        is triggered at the end of timer
        """
        self.timer_is_done = True

    def query(self, cmd, print_and_log=True):
        """Send the input cmd string via TCPIP Socket
        @type cmd: string
        @param cmd: command to send to printer
        @type print_and_log: bool
        @param print_and_log: if true print and log the communication
        @return: the reply string
        """
        if print_and_log:
            msg = "Sent command to printer: " + cmd.strip('\r\n')
            printing_func(msg, 'PrinterThread', lock_print, logger_type='debug',
                          logger_name=self.ports_and_guis.my_logger.logger.name)
        self.ports_and_guis.Printer_socket.send(cmd.encode())
        data = self.ports_and_guis.Printer_socket.recv(int(self.TCP_BUFFER))
        if len(data) == 0:
            raise PrinterNeedsResetException(f'The printer did not ack to the following cmd :{cmd}')
        value = data.decode("utf-8")
        # Cut the last character as the device returns a null terminated string
        value = value[:-1]
        if print_and_log:
            msg = "Received answer from printer: " + str(value.strip('\r\n'))
            printing_func(msg, 'PrinterThread', lock_print, logger_type='debug',
                          logger_name=self.ports_and_guis.my_logger.logger.name)

        return value

    def closure(self):
        """
        set printer to shutting down and close the socket
        """
        try:
            self.query(self.set_state_command('2'))  # for regular closure (not when connection error happens)
            self.ports_and_guis.Printer_socket.close()
        except Exception:
            try:
                self.ports_and_guis.Printer_socket.close()
            except Exception:
                printing_func('s.close() failed', 'PrinterThread', lock_print, logger_type='warning',
                              logger_name=self.ports_and_guis.my_logger.logger.name)
                pass

    def reopen_sock(self):
        """
        close and reopens the printer sock
        """
        try:
            self.closure()
            time.sleep(1)  # to make sure the socket is closed when we start the reopen
            self.initialization()
        except Exception:
            printing_func('reopen_sock() failed, please end this run', 'PrinterThread',
                          lock_print, logger_type='warning', logger_name=self.ports_and_guis.my_logger.logger.name)
            raise (PrinterNeedsResetException('reopen_sock() failed'))

    # UNUSED FUNCTION
    def line_assigment(self, job_name, line_number, field_name, field_value):
        """
        builds the command to send to printer for configuration of the printing format
        @param job_name: (string) what is the job name (should be the same as in the printer)
        @param line_number: what is the line to assign to (2 = pass, 1 = fail)
        @param field_name: field name in the printer
        @param field_value: what to put in this field
        @return: the cmd to send to printer
        """
        # Send Line Assignment Command: job name + line number+starting value
        cmd = 'LAS|' + str(job_name) + '|' + str(line_number) + '|' + str(field_name) + '=' + str(
            field_value) + '|\r\n'
        # changing to bytes
        return cmd

    # UNUSED FUNCTION
    def clear_line(self, line_number):
        """
        builds the command to send to printer for clearing a line
        @param line_number: the line to clear
        @return: the cmd to send to printer
        """
        # On success, returns the default success response (ACK). On failure, returns the default failure response (ERR)
        cmd = 'CLN|' + str(line_number) + '|\r\n'
        return cmd

    def set_state_command(self, desired_state):
        """
        builds the command to send to printer for setting a printer state
        @param desired_state: the state to enter to, according to the following description
        0 Shut down
        1 Starting up
        2 Shutting down
        3 Running
        4 Offline
        @return: the cmd to send to printer
        """
        cmd = 'SST|' + str(desired_state) + '|\r\n'
        return cmd

    # UNUSED FUNCTION
    def get_job_name(self):
        """
        gets the last job that were used by the printer
        @return: the name of the current job in the printer in the following format:
            JOB|<job name>|<line number>|<CR>
        """
        cmd = 'GJN\r\n'
        return cmd

    def get_state_request(self):
        """
        gets the situation of the printer
        @return: the situation in the printer in the following format:
            STS|<overallstate>|<errorstate>|<currentjob>|<batchcount>|<totalcount>|<
        """
        cmd = 'GST\r\n'
        return cmd


class TagThread(threading.Thread):
    """
    Thread that controls the gateway, tests each tag and saves data to csv output file
    Parameters:
        @type events: class MainEvents (costume made class that has all of the Events of the program threads)
        @param events: has all of the Events of the program threads
        @type ports_and_guis: class PortsAndGuis (costume made class that has all of the ports and gui inputs for the
                            program threads)
        @param ports_and_guis: has all of the ports and gui inputs for the program threads

    Exceptions:
        @except Exception: 'Exception happened in Tag thread initialization. need to kill this run'
                means that connecting to GW or temperature sensor failed, the run will pause and wait for
                stop button from user

        @except Exception: 'tag_checker_thread got an Exception, press Continue or Stop'
                exception details will be printed

        @except (OSError, serial.SerialException):
                Problems with GW connection, requires user to press "Stop" and end the run

        @except Exception: exception occurred while testing a tag (inside new_tag function)

        @except Exception('R2R moved before timer ended') :
                Either R2R moved before or received packet is not valid tag packet
                The run will pause

        @except Exception: 'Warning: packet_decoder could not decode packet, will skip it'
                In case encrypted_packet_decoder() failed in decoding packet, packet is skipped and
                threads waits for next packet.
                Run won't pause in that case. If tag reaches timeout, it will marked as fail

    Events:
        listen/ waits on:
            events.r2r_ready_or_done2tag => user pressed Stop (end the program) or r2r has finished to write the command
            events.done_or_printer_event => waits for printer event or for done_to_tag_thread (closes TagThread)
            events.done_to_tag_thread => closes TagThread at the end of the run
            events.printer_error => the last print was not successful, will cause pause to this run
                                                (and will trigger exception according to the situation)

        sets:
            events.tag_thread_is_ready_to_main => notifies MainWindow thread TagThread is ready
            events.was_pass_to_printer => tag has passed. report "Pass" to printer
            events.was_fail_to_printer => tag has failed. report "Fail" to printer
            events.disable_missing_label_to_r2r_thread => if set, the run will pause if missing label is detected
            events.enable_missing_label_to_r2r_thread => if set, the run will not pause if missing label is detected
                                                        (up to maxMissingLabels set by user)
            events.start_to_r2r_thread => enable/disable R2R movement. Sends pulse on "Start/Stop machine" GPIO line
            events.stop_to_r2r_thread => stops the R2R from running in case of end of run or exception
            events.pass_to_r2r_thread => notify if current tag passed. if set, send pulse on "Pass" GPIO line,
                                         The R2R will advance to next tag
            events.fail_to_r2r_thread => notify if current tag failed. if set, send pulse on "Fail" GPIO line,
                                         The R2R will advance to next tag

    Logging:
        logging to logging.debug(), logging.info() and logging.warning()
    """

    def __init__(self, events, ports_and_guis, management_client=None):
        """
        Initialize Constants
        """
        super(TagThread, self).__init__(daemon=True)
        self.ports_and_guis = ports_and_guis
        self.events = events
        # self.test_times_up = False
        self.r2r_response_times_up = False
        self.test_suite_times_up = False
        self.duplication_handling_timer_is_done = False
        self.ttfgp_list = []
        self.black_list = []
        self.adv_addr = ''
        self.ttfp_num = 0
        self.ttfp_sum = 0
        self.rssi = 0
        self.tbp = -1
        self.ttfp = -1
        self.time_for_duplication_handling = 20  # time in seconds for duplication handling procedure
        self.management_client = management_client
        self.fatal_gw_error = False
        self.pass_response_diff_offset = None
        self.pass_response_diff = None

        self.pass_job_name = ''  # will be set inside config
        self.to_print = False
        self.printing_value = {'passJobName': None, 'stringBeforeCounter': None, 'digitsInCounter': 4,
                               'firstPrintingValue': '0'}  # will be set in config()
        self.done_or_printer_event = or_event_set(self.events.done_to_tag_thread, self.events.printer_event)
        self.fetal_error = False
        self.exception_queue = Queue()
        self.qr_enable = self.ports_and_guis.Tag_Value['QRRead']
        self.qr_offset = self.ports_and_guis.Tag_Value['QRoffset']
        self.printing_offset = self.ports_and_guis.Tag_Value['printOffset']
        self.qr_max_bad_tags = int(self.ports_and_guis.Tag_Value['maxQRWrongTags'])
        self.maxblackappear = int(self.ports_and_guis.Tag_Value['blackListAfter'])
        self.events.tag_status_queue.maxsize = int(self.printing_offset) + 1
        if self.qr_enable == 'Yes':
            self.events.qr_queue.maxsize = int(self.qr_offset) + 1
        else:
            self.events.qr_queue.maxsize = int(self.printing_offset) + 1
            for i in range(self.printing_offset + 1):
                self.events.qr_queue.put({'status': 'Fail'})
        for i in range(self.printing_offset):  # first printed tag is checked upon init
            self.events.tag_status_queue.put('fail')
        self.did_closure_fn_run = False

        self.packet_headers_default = \
            ['common_run_name', 'tag_run_location', 'tag_reel_location', 'test_num', 'external_id', 'time_from_start',
             'raw_packet', 'rssi',
             'packet_status', 'adv_address', 'selected_tag', 'is_test_pass', 'status_offline', 'fail_bin',
             'fail_bin_str',
             'test_status', 'num_packets', 'num_cycles', 'sprinkler_counter_mean', 'sprinkler_counter_std',
             'sprinkler_counter_min', 'sprinkler_counter_max', 'tbp_mean', 'tbp_std', 'tbp_min', 'tbp_max',
             'tbp_num_vals',
             'per_mean', 'per_std', 'rssi_mean', 'rssi_std', 'rssi_min', 'rssi_max', 'ttfp', 'rx_rate_normalized',
             'rx_rate', 'total_test_duration', 'total_location_duration', 'test_start_time', 'trigger_time',
             'test_end_time', 'label_validated_at_loc', 'rx_channel', 'energizing_pattern', 'time_profile',
             'decrypted_packet_type',
             'group_id', 'flow_ver', 'test_mode', 'en', 'type', 'data_uid', 'nonce', 'enc_uid', 'mic', 'enc_payload',
             'gw_packet', 'stat_param', 'temperature_sensor']

        try:
            self.GwObj, self.t = self.config()

            self.WiliotTester = WiliotTesterTagTest(
                selected_test=self.ports_and_guis.Tag_Value['inlayType'],
                test_suite=self.ports_and_guis.all_tests_suites,
                gw_obj=self.GwObj,
                logger_name=self.ports_and_guis.my_logger.logger.name,
                logger_result_name=self.ports_and_guis.my_logger.results_logger.name,
                logger_gw_name=self.ports_and_guis.my_logger.gw_logger.name,
                stop_event_trig=self.events.done_to_r2r_thread,
                inlay=InlayTypes(self.ports_and_guis.Tag_Value['inlay']).name)
            self.all_selected_tags = []
            self.all_tags = []
            global run_start_time_
            self.loc_start_time_ = run_start_time_

        except Exception as e:
            exception_details = sys.exc_info()
            self.exception_queue.put(exception_details)
            printing_func(
                'Exception happened in Tag thread initialization. need to kill this run. {}'.format(
                    format_exception_details(exception_details)),
                'TagThread', lock_print, logger_type='warning', logger_name=self.ports_and_guis.my_logger.logger.name)
            # to pause the run if exception happens
            self.events.done_to_tag_thread.set()
            self.events.stop_to_r2r_thread.set()

        self.r2r_timer = None
        self.test_suites_timer = None
        self.timer_for_curr_test = ''
        # self.printed_external_id = ''
        self.next_printed_external_id = ''
        self.timer_for_duplication_handling = None
        self.fail_tags_with_same_packet_within_secs = False
        self.enable_line_selection = self.ports_and_guis.Tag_Printing_Value['enableLineSelection'].lower() == 'yes' \
            if self.to_print else False

        self.tag_location = 0
        self.events.tag_thread_is_ready_to_main.set()

    def call_printer_validation(self):
        if self.to_print and not self.ports_and_guis.print_test:
            self.events.printer_validation_success.clear()
            self.events.qr_read_success.clear()
            if self.qr_enable == 'Yes':
                if self.events.qr_queue.full():
                    self.events.start_compare.set()  # start qr readout
                    self.ports_and_guis.my_logger.logger.info('Sent start to test QR')
                else:
                    self.events.qr_read_success.set()
                    self.ports_and_guis.my_logger.logger.info('Queue not full yet')

            else:
                self.events.start_compare.set()
        elif self.qr_enable == 'Yes' and not self.ports_and_guis.print_test:
            self.events.printer_validation_success.clear()
            self.events.qr_read_success.clear()
            self.events.start_compare.set()

    def check_printer_validation(self):
        if self.to_print and not self.ports_and_guis.print_test:
            self.events.validation_success.wait(timeout=5)
            if not self.events.validation_success.isSet():
                self.ports_and_guis.my_logger.logger.warning(
                    "QR Validation didn't succeed or Printer counter is not right")
                self.events.stop_to_r2r_thread.set()
                self.events.done_to_tag_thread.set()
            else:
                self.ports_and_guis.my_logger.logger.info('Validation criteria is ok')
            self.events.printer_validation_success.clear()
            self.events.qr_read_success.clear()

    def check_qr_validation(self):
        if self.qr_enable == 'Yes' and not self.to_print:
            self.events.validation_success.wait(timeout=5)
            if not self.events.validation_success.isSet():
                self.ports_and_guis.my_logger.logger.warning(
                    "QR Validation didn't succeed or Printer counter is not right")
            else:
                self.ports_and_guis.my_logger.logger.info('Validation criteria is ok')
            self.events.printer_validation_success.clear()
            self.events.qr_read_success.clear()

    @pyqtSlot()
    def run(self):
        """
        runs the thread
        """
        global problem_in_locations_hist, fail_bin_list
        problem_in_locations_hist = {'NO_RESPONSE': 0, 'NO_PACKETS_UNDER_RSSI_THR': 0, 'MISSING_LABEL': 0,
                                     'DUPLICATION_OFFLINE': 0, 'GW_ERROR': 0, 'SEVERAL_TAGS_UNDER_TEST': 0}
        fail_bin_list = []
        if self.value['missingLabel'] == 'No':
            self.events.disable_missing_label_to_r2r_thread.set()
            self.is_missing_label_mode = False
        elif self.value['missingLabel'] == 'Yes':
            self.events.enable_missing_label_to_r2r_thread.set()
            self.is_missing_label_mode = True
        self.first_tag = True
        self.events.tag_thread_is_ready_to_main.set()
        die = False
        self.missing_labels_in_a_row = 0
        self.time_out_to_missing_label = 2.5
        if 'wait_for_gw_trigger' in self.ports_and_guis.Tag_Value:
            wait_for_gw_trigger = float(self.ports_and_guis.Tag_Value['wait_for_gw_trigger'])
        else:
            wait_for_gw_trigger = self.time_out_to_missing_label
        self.ports_and_guis.my_logger.logger.info('Maximum time for gw trigger (i.e. missing label) is {}'.
                                                  format(wait_for_gw_trigger))
        self.next_printed_external_id = self.printed_external_id

        while not die:
            try:
                time.sleep(0)
                self.events.r2r_ready_or_done2tag.wait()
                if self.events.done_to_tag_thread.is_set():
                    self.ports_and_guis.my_logger.logger.warning('TagThread recieved - Job is done')
                    die = True
                    break
                else:  # the r2r_ready event happened , done_or_printer_event.wait will happen after start GW
                    # start of tags loop ###########################
                    # the long timer (will cause +1 missing label)
                    global tested, passed, missing_labels, black_list_size, responded
                    global last_pass_string, reel_name
                    self.events.r2r_ready.clear()
                    self.r2r_response_times_up = False
                    self.start_GW_happened = False
                    # will wait 10 seconds after the tag timer should have ended
                    # and then will enforce a start_r2r & fail_r2r

                    # self.r2r_timer = threading.Timer(self.time_out_to_missing_label, self.end_of_time,
                    #                                  ['r2r is stuck'])
                    # self.r2r_timer.start()
                    self.start_time = datetime.datetime.now()

                    if self.events.done_to_tag_thread.is_set():
                        break
                    self.ports_and_guis.my_logger.results_logger.info(
                        '******************** New tag test starts at location: {}, excpected externalID is: {} ******'
                        '**************'.format(
                            str(self.tag_location), str(self.next_printed_external_id)))

                    if self.ports_and_guis.energizerGW:
                        if 'DelayBeforeTest' in self.ports_and_guis.tests_suite['additionalGW']:
                            time.sleep(int(self.ports_and_guis.tests_suite['additionalGW']['DelayBeforeTest']))

                    if self.extended_test:
                        self.ports_and_guis.my_logger.logger.info('Waiting for pulse')
                        self.pulse_received = self.WiliotTester.wait_for_trigger(wait_for_gw_trigger)
                        if self.pulse_received:
                            self.ports_and_guis.my_logger.logger.info('Pulse received')
                            self.events.stop_to_test_r2r_thread.set()
                            while self.events.stop_to_test_r2r_thread.is_set():
                                time.sleep(0.01)
                                pass
                            self.tester_res = self.WiliotTester.run(wait_for_gw_trigger=None,
                                                                    need_to_manual_trigger=False)
                            self.events.start_to_test_r2r_thread.set()
                            while self.events.start_to_test_r2r_thread.is_set():
                                time.sleep(0.01)
                                pass
                        else:
                            self.ports_and_guis.my_logger.logger.info("Pulse didn't received")
                            self.tester_res = WiliotTesterTagResultList()  # Empty list

                    else:
                        # get trigger:
                        self.ports_and_guis.my_logger.logger.info('Waiting for pulse')
                        self.pulse_received = self.WiliotTester.wait_for_trigger(wait_for_gw_trigger)
                        self.call_printer_validation()
                        if self.pulse_received:
                            self.ports_and_guis.my_logger.logger.info('Pulse received')
                            if self.ports_and_guis.energizerGW:
                                if self.ports_and_guis.additional_gw_mode == DualGWMode.DYNAMIC:
                                    self.stop_energizer()
                                elif self.ports_and_guis.additional_gw_mode == DualGWMode.MIRROR:
                                    self.start_energizer()
                                elif self.ports_and_guis.additional_gw_mode == DualGWMode.STATIC and 'lite_power' in \
                                        self.tests_suite['additionalGW']:
                                    self.ports_and_guis.energizerGW.config_gw(
                                        output_power_val=self.tests_suite['additionalGW']['lite_power'])

                            # start tag test
                            self.tester_res = self.WiliotTester.run(wait_for_gw_trigger=None,
                                                                    need_to_manual_trigger=False)
                        else:
                            self.ports_and_guis.my_logger.logger.info("Pulse didn't received")
                            self.tester_res = WiliotTesterTagResultList()  # Empty list
                    # end tag test

                    if self.ports_and_guis.energizerGW:
                        if self.ports_and_guis.additional_gw_mode == DualGWMode.DYNAMIC:
                            self.start_energizer()
                        elif self.ports_and_guis.additional_gw_mode == DualGWMode.MIRROR:
                            self.stop_energizer()
                        elif self.ports_and_guis.additional_gw_mode == DualGWMode.STATIC and 'lite_power' in \
                                self.tests_suite['additionalGW']:
                            self.ports_and_guis.energizerGW.config_gw(
                                output_power_val=self.tests_suite['additionalGW']['gw_output_power'])

                        if 'DelayAfterTest' in self.ports_and_guis.tests_suite['additionalGW']:
                            time.sleep(self.ports_and_guis.tests_suite['additionalGW']['DelayAfterTest'])

                    if self.ports_and_guis.temperature_enabled:
                        # self.ports_and_guis.my_logger.logger.debug('Receiving tempreture data from sensor')
                        try:
                            temperature_sensor = get_temperature()
                            # self.ports_and_guis.my_logger.logger.info(temperature_sensor)
                        except Exception:
                            self.ports_and_guis.my_logger.logger.warning('Problem with temperature sensor detection')
                            pass
                        self.ports_and_guis.my_logger.logger.debug('Temperature is: {}'.format(str(temperature_sensor)))
                    else:
                        temperature_sensor = float(-1)

                    if self.qr_enable == 'Yes' and not self.to_print:
                        self.check_qr_validation()

                    self.test_data['tag_run_location'] = self.tag_location
                    self.test_data['tag_reel_location'] = int(self.tag_reel_location) + int(self.tag_location)
                    self.test_data['temperature_sensor'] = temperature_sensor
                    if self.events.done_to_tag_thread.is_set():
                        break
                    # printing processes:
                    if self.to_print and not self.ports_and_guis.print_test:
                        self.test_data['external_id'] = self.printed_external_id
                        self.ports_and_guis.my_logger.logger.info('Making sure printer or QR doesnt have failures')
                        self.check_printer_validation()
                    elif self.to_print and self.ports_and_guis.print_test:
                        self.test_data['external_id'] = self.printed_external_id


                    try:
                        if self.events.done_to_tag_thread.is_set():
                            break
                        tested += 1
                        if self.tester_res.is_results_empty():
                            missing_labels += 1
                            self.missing_labels_in_a_row += 1
                            self.ports_and_guis.my_logger.logger.info('Missing label')
                            self.run_data['total_missing_labels'] = missing_labels
                            self.test_data['fail_bin'] = FailureCodes.MISSING_LABEL.value
                            self.test_data['fail_bin_str'] = FailureCodes.MISSING_LABEL.name
                            self.test_data['is_test_pass'] = False
                            self.ports_and_guis.my_logger.logger.warning(
                                'Tag location: {} failed - Missing Label'.format(str(self.tag_location)))
                            self.events.start_to_r2r_thread.set()

                            total_loc_time = datetime.datetime.now() - self.start_time
                            self.test_data['total_location_duration'] = total_loc_time.total_seconds()
                            self.test_data['label_validated_at_loc'] = self.events.qr_val.is_set()
                            # add packets to packet_data.csv:
                            self.update_packet_data(packets_data_path=self.ports_and_guis.my_logger.packets_data_path,
                                                    test_data=self.test_data)
                            # update run_data:
                            self.update_run_data(run_data_path=self.ports_and_guis.my_logger.run_data_path,
                                                 run_data=self.run_data)
                            if self.to_print and not self.ports_and_guis.print_test:
                                self.events.qr_queue.put({'externalID': 'Missing Label', 'status': 'Fail'})
                                if self.enable_line_selection:
                                    self.events.tag_status_queue.put('fail')
                                self.ports_and_guis.my_logger.logger.debug('Added missing label to que as fail')
                            # self.events.enable_missing_label_to_r2r_thread.set()
                            if self.missing_labels_in_a_row >= int(self.value['maxMissingLabels']):
                                self.ports_and_guis.my_logger.logger.warning('Max missing labels were detected')
                                self.events.done_to_r2r_thread.set()
                                self.events.done_to_tag_thread.set()
                                if self.to_print:
                                    self.events.done_to_printer_thread.set()

                            if not self.is_missing_label_mode:
                                self.ports_and_guis.my_logger.logger.warning('Run stopped due to missing label')
                                self.events.done_to_tag_thread.set()
                                self.events.done_to_r2r_thread.set()
                                if self.to_print:
                                    self.events.done_to_printer_thread.set()

                        else:
                            cur_ttfp = self.tester_res.get_total_ttfp()
                            if cur_ttfp is not None:
                                self.ttfp_sum = self.ttfp_sum + cur_ttfp
                                self.ttfp_num = self.ttfp_num + 1

                            if self.ttfp_num:
                                self.run_data['ttfp_avg'] = self.ttfp_sum / self.ttfp_num

                            selected_tag = self.tester_res.check_and_get_selected_tag_id()
                            if selected_tag == '':
                                # Didnt understand who is talking in different stages or the case no tag was selected
                                # responded += 1
                                try:
                                    self.ports_and_guis.my_logger.logger.warning(
                                        'Tag location: {} failed - {}'.format(self.tag_location,
                                                                              self.tester_res.get_total_fail_bin(
                                                                                  as_name=True)))
                                except Exception:
                                    pass
                                if self.to_print and not self.ports_and_guis.print_test:
                                    self.events.qr_queue.put({'externalID': '', 'status': 'Fail'})
                                    if self.enable_line_selection:
                                        self.events.tag_status_queue.put('fail')
                                    self.ports_and_guis.my_logger.logger.debug(
                                        'Tag added as fail')
                                self.events.fail_to_r2r_thread.set()

                            else:
                                if selected_tag in self.all_selected_tags:
                                    # Duplication
                                    self.tester_res.set_total_fail_bin(FailureCodes.DUPLICATION_OFFLINE)
                                    self.tester_res.set_total_test_status(status=False)
                                    black_list_size += 1
                                    self.black_list.append(selected_tag)
                                    self.ports_and_guis.my_logger.logger.warning(
                                        'Tag location: {} has been already seen in the run before'.format(
                                            str(self.tag_location)))
                                    self.tester_res.set_packet_status(adv_address=selected_tag,
                                                                      status='duplication')
                                    if self.to_print and not self.ports_and_guis.print_test:
                                        self.events.qr_queue.put({'externalID': selected_tag, 'status': 'Fail'})
                                        if self.enable_line_selection:
                                            self.events.tag_status_queue.put('fail')

                                    if int(self.black_list.count(selected_tag)) >= self.maxblackappear:
                                        self.WiliotTester.add_to_blacklist(selected_tag)
                                        self.ports_and_guis.my_logger.logger.warning(
                                            'Tag {} in location {} has reached max appearance in black list'.format(
                                                selected_tag, self.tag_location))
                                    self.events.fail_to_r2r_thread.set()

                                else:
                                    responded += 1
                                    # Tag pass or fail but with respond
                                    self.missing_labels_in_a_row = 0
                                    self.all_selected_tags.append(selected_tag)
                                    if self.tester_res.is_all_tests_passed():
                                        # Pass
                                        passed += 1
                                        if self.to_print and not self.ports_and_guis.print_test:

                                            self.printed_external_id, is_OK = get_printed_value(
                                                self.printing_value['stringBeforeCounter'],
                                                self.printing_value['digitsInCounter'],
                                                str(self.externalId),
                                                self.value['printingFormat'])
                                            self.next_printed_external_id, is_OK = get_printed_value(
                                                self.printing_value['stringBeforeCounter'],
                                                self.printing_value['digitsInCounter'],
                                                str(int(self.externalId) + 1),
                                                self.value['printingFormat'])
                                            self.test_data['external_id'] = self.printed_external_id

                                            last_pass_string = f'advAddress: {str(selected_tag)} , Tag Location:  ' \
                                                               f'{str(self.tag_location)} , External ID: {self.printed_external_id} '
                                            # f', RSSI: 'f'{self.rssi}, TBP: {self.tbp}, TTFP: {self.ttfp}'
                                            self.events.qr_queue.put(
                                                {'externalID': self.printed_external_id, 'status': 'Pass'})
                                            if self.enable_line_selection:
                                                self.events.tag_status_queue.put('pass')
                                            self.ports_and_guis.my_logger.logger.info(
                                                'Added tag {} to que as pass'.format(self.printed_external_id))
                                            self.externalId += 1
                                        else:
                                            last_pass_string = f'Tag Location:  {str(self.tag_location)}'
                                            self.printed_external_id, is_OK = get_printed_value(
                                                self.printing_value['stringBeforeCounter'],
                                                self.printing_value['digitsInCounter'],
                                                str(self.externalId),
                                                self.value['printingFormat'])
                                            self.next_printed_external_id, is_OK = get_printed_value(
                                                self.printing_value['stringBeforeCounter'],
                                                self.printing_value['digitsInCounter'],
                                                str(int(self.externalId) + 1),
                                                self.value['printingFormat'])
                                            self.test_data['external_id'] = self.printed_external_id
                                            self.externalId += 1
                                        self.events.pass_to_r2r_thread.set()
                                    else:
                                        # Tag failed statistics
                                        self.ports_and_guis.my_logger.logger.warning(
                                            'Tag location: {} failed - {}'.format(str(self.tag_location), str(
                                                self.tester_res.get_total_fail_bin(as_name=True))))
                                        if self.to_print and not self.ports_and_guis.print_test:
                                            self.events.qr_queue.put({'externalID': '', 'status': 'Fail'})
                                            if self.enable_line_selection:
                                                self.events.tag_status_queue.put('pass')

                                            self.ports_and_guis.my_logger.logger.debug(
                                                'Tag added as fail, failed during test')
                                        self.events.fail_to_r2r_thread.set()
                            self.all_tags += self.tester_res.get_test_unique_adva()
                            self.all_tags = list(set(self.all_tags))
                            self.run_data['total_run_responding_tags'] = len(self.all_tags)
                            total_loc_time = datetime.datetime.now() - self.start_time
                            self.test_data['total_location_duration'] = total_loc_time.total_seconds()
                            self.test_data['label_validated_at_loc'] = self.events.qr_val.is_set()
                            # add packets to packet_data.csv:
                            self.update_packet_data(res=self.tester_res,
                                                    packets_data_path=self.ports_and_guis.my_logger.packets_data_path,
                                                    test_data=self.test_data)
                            # update run_data:
                            self.update_run_data(run_data_path=self.ports_and_guis.my_logger.run_data_path,
                                                 run_data=self.run_data, res=self.tester_res)
                        self.tag_location += 1
                        # Check the diff criteria
                        if self.pass_response_diff is not None:
                            if len(self.all_tags) > self.pass_response_diff_offset:
                                if (passed * 100) / len(self.all_tags) < 100 - int(self.pass_response_diff):
                                    self.ports_and_guis.my_logger.logger.warning(
                                        'Problem with setup, stop criteria for responsive tags and pass tags diff is '
                                        'lower then threshold please check setup or change the value')
                                    self.events.done_to_r2r_thread.set()
                                    self.events.done_to_tag_thread.set()
                                    if self.to_print:
                                        self.events.done_to_printer_thread.set()
                        # update extended results:
                        if self.tester_res.is_results_empty():
                            fail_bin_list.append(FailureCodes.MISSING_LABEL.name)
                        else:
                            fail_bin_list.append(self.tester_res.get_total_fail_bin(as_name=True))

                        # end of tags loop ###############################

                    except Exception as e:
                        self.ports_and_guis.my_logger.logger.warning('Run stopped due to the following '
                                                                     'Exception: {}'.format(e))
                        self.events.done_to_tag_thread.set()
                        self.events.done_to_r2r_thread.set()
                        self.events.done_to_printer_thread.set()
                        raise e

            except (OSError, serial.SerialException):
                if self.events.done_to_tag_thread.is_set():
                    self.ports_and_guis.my_logger.logger.warning('TagThread recieved - Job is done (OSError)')
                    die = True
                exception_details = sys.exc_info()
                self.exception_queue.put(exception_details)
                printing_func("Problems with gateway serial connection - click on Stop and exit the app. {}".format(
                    format_exception_details(exception_details)),
                    'TagThread', lock_print, logger_type='warning',
                    logger_name=self.ports_and_guis.my_logger.logger.name)
                self.fetal_error = True
            except Exception:
                if self.events.done_to_tag_thread.is_set():
                    self.ports_and_guis.my_logger.logger.warning('TagThread recieved - Job is done (Exception)')
                    die = True
                exception_details = sys.exc_info()
                self.exception_queue.put(exception_details)
                # wait until user press Continue
                if self.r2r_timer is not None:
                    self.r2r_timer.cancel()

        self.closure_fn()

    def end_of_time(self, kind):
        """
        sets the correct flag to True when a timer is done
        @param kind: the kind of the timer
        """
        if kind == 'tag':
            self.test_suite_times_up = True
            printing_func("Tag reached Time-Out",
                          'TagThread', lock_print, logger_type='debug',
                          logger_name=self.ports_and_guis.my_logger.logger.name)
        if kind == 'r2r is stuck':
            self.r2r_response_times_up = True
            printing_func("R2R is stuck, Tag reached Time-Out",
                          'TagThread', lock_print, logger_type='debug',
                          logger_name=self.ports_and_guis.my_logger.logger.name)
            self.ports_and_guis.my_logger.logger.debug("R2R is stuck, Tag reached Time-Out")
        if kind == 'duplication handling':
            self.duplication_handling_timer_is_done = True
            printing_func("Duplication handling timer is over",
                          'TagThread', lock_print, logger_type='debug',
                          logger_name=self.ports_and_guis.my_logger.logger.name)

    def config(self):
        """
        configuration of GW, logging and run_data
        @return:  Gw's Com port Obj, temperature sensor
        """
        self.value = self.ports_and_guis.Tag_Value
        if self.value['comments'] == '':
            self.value['comments'] = None

        self.tests_suite = self.ports_and_guis.tests_suite
        if int(self.ports_and_guis.total_time) >= 98:
            self.extended_test = True
        else:
            self.extended_test = False
        if 'rssiThresholdSW' not in self.tests_suite:
            raise Exception('rssiThresholdSW should be specified in the test suite')
        if 'rssiThresholdHW' not in self.tests_suite:
            raise Exception('rssiThresholdHW should be specified in the test suite')

        self.num_of_tests = len(self.tests_suite['tests'])
        for test_num in range(self.num_of_tests):
            if not 'absGwTxPowerIndex' in self.tests_suite['tests'][test_num]:
                if 'tbpTarget' in self.tests_suite['tests'][test_num]:
                    top_score = get_calibration_results(target_tbp=self.tests_suite['tests'][test_num]['tbpTarget'],
                                                        energy_pattern=[
                                                            self.tests_suite['tests'][test_num]['energizingPattern']])
                else:
                    self.ports_and_guis.my_logger.logger.info(
                        'Problem with generating tbp best power from config file will work with default calibration knee')
                    top_score = get_calibration_results(target_tbp=0, energy_pattern=[
                        self.tests_suite['tests'][test_num]['energizingPattern']])

                self.tests_suite['tests'][test_num]['absGwTxPowerIndex'] = top_score['absGwTxPowerIndex'].item()
                if not 'timeProfile' in self.tests_suite['tests'][test_num]:
                    self.tests_suite['tests'][test_num]['timeProfile'][0] = top_score['time_profile_on'].item()
                    self.tests_suite['tests'][test_num]['timeProfile'][1] = top_score['time_profile_period'].item()

                self.ports_and_guis.my_logger.logger.info(
                    'values set for test {} are: tbp_target = {}, top score index = {}, rssi_threshold_hw = {}, rssi_threshold_sw = {}'.format(
                        str(test_num),
                        str(top_score[
                                'tbp_mean'].item()),
                        str(
                            self.tests_suite[
                                'tests'][
                                test_num][
                                'absGwTxPowerIndex']), self.tests_suite['rssiThresholdHW'],
                        self.tests_suite['rssiThresholdSW']))
                if (not 'absGwTxPowerIndex' in self.tests_suite['tests'][test_num]) and (
                        not 'tbpTarget' in self.tests_suite['tests'][test_num]):
                    self.ports_and_guis.my_logger.logger.warning('Please setup test suite tests or calibrate machine')

            else:
                self.ports_and_guis.my_logger.logger.info(
                    'values set for test {} are: top score index = {}'.format(str(test_num), str(
                        self.tests_suite['tests'][test_num]['absGwTxPowerIndex'])))

        self.internal_value = {"energizingPattern": "-1", "timeProfile": "-1", "txPower": "-1", "rssiThresholdHW":
            str(self.tests_suite['rssiThresholdHW']), "rssiThresholdSW": str(self.tests_suite['rssiThresholdSW']),
                               "plDelay": str(self.tests_suite['plDelay'])}
        # for the case we do not print
        self.externalId = 0
        self.pass_job_name = ''
        self.tag_reel_location = 0
        if self.value['toPrint'] == 'Yes':
            self.to_print = True
            self.printing_value, is_OK = self.ports_and_guis.Tag_Printing_Value, self.ports_and_guis.Tag_is_OK
            self.externalId = int(self.printing_value['firstPrintingValue'])
            self.pass_job_name = self.printing_value['passJobName']
            self.tag_reel_location = int(self.printing_value['tag_reel_location'])

        if 'pass_response_diff' in self.ports_and_guis.Tag_Value:
            try:
                self.pass_response_diff = int(self.ports_and_guis.Tag_Value['pass_response_diff'])
            except Exception as e:
                self.ports_and_guis.my_logger.logger.warning(f'Could not convert the pass_response_diff to number, '
                                                             f'the defualt value would be 10: {e}')
                self.pass_response_diff = 10
            if 'pass_response_diff_offset' in self.ports_and_guis.Tag_Value:
                self.pass_response_diff_offset = int(self.ports_and_guis.Tag_Value['pass_response_diff_offset'])
            else:
                self.pass_response_diff_offset = 100
        else:
            self.pass_response_diff = None

        # setting up the global variables ###################################################
        global desired_pass_num
        global desired_tags_num
        desired_tags_num = int(self.value['desiredTags'])
        desired_pass_num = int(self.value['desiredPass'])

        # config GW, temp sens and classifier ###############################################
        self.GwObj = self.ports_and_guis.GwObj

        global temperature_sensor_enable
        if temperature_sensor_enable:
            t = self.ports_and_guis.Tag_t
        else:
            t = None
        self.internal_value['testerStationName'] = self.ports_and_guis.tag_tester_station_name

        printing_func("wiliot's package version = " + str(get_version()), 'TagThread', lock_print=lock_print,
                      do_log=True, logger_name=self.ports_and_guis.my_logger.logger.name)
        global run_start_time
        self.ports_and_guis.my_logger.logger.info('Start time is: ' + run_start_time + ', User set up is: %s, %s, %s',
                                                  self.value, self.internal_value, self.printing_value)
        self.run_data_init()
        self.update_run_data(run_data_path=self.ports_and_guis.my_logger.run_data_path, run_data=self.run_data)
        self.update_packet_data(packets_data_path=self.ports_and_guis.my_logger.packets_data_path, only_titles=True,
                                test_data=self.test_data)

        if self.ports_and_guis.auto_attenuator_enable:
            attn_pwr = int(self.ports_and_guis.Tag_Value['attnval']) - 5
            self.ports_and_guis.my_logger.results_logger.info('Setting ATTN to {}'.format(attn_pwr))
            set_attn_status = self.ports_and_guis.attenuator.Setattn(attn_pwr)
            time.sleep(2)
            if set_attn_status:
                self.ports_and_guis.my_logger.results_logger.info(
                    'Attenuation in dB set to {}'.format(self.ports_and_guis.attenuator.Getattn()))

        self.ttfp_num = 0
        self.ttfp_sum = 0
        return self.GwObj, t

    def start_energizer(self):
        if self.ports_and_guis.energizerGW:
            self.ports_and_guis.energizerGW.write('!gateway_app')

    def stop_energizer(self):
        if self.ports_and_guis.energizerGW:
            self.ports_and_guis.energizerGW.write('!cancel')
            self.ports_and_guis.energizerGW.reset_buffer()

    def get_curr_timestamp_in_sec(self):
        return (datetime.datetime.now() - self.start_time).total_seconds()

    # UNUSED FUNCTION
    def is_gw_respond_with_stat_param_zero(self, chosen_tag_packets):
        chosen_tag_packets_df = chosen_tag_packets.get_df()
        return len(chosen_tag_packets_df[chosen_tag_packets_df['stat_param'] == 0]) > 1

    def closure_fn(self):
        """
           turn off the GW (reset) and closes the GW Comport
           Logging:
               'User pressed Stop!'
           """
        if self.black_list.__len__() > 0:
            self.ports_and_guis.my_logger.logger.warning('Black list tags: {}'.format(list(set(self.black_list))))
        if not self.did_closure_fn_run:
            self.run_data['reel_run_end_time'] = datetime.datetime.now()
            self.run_data['upload_date'] = datetime.datetime.now()
            dict_to_csv(self.run_data, path=self.ports_and_guis.my_logger.run_data_path)
            self.WiliotTester.exit_tag_test()
            printing_func("TagThread is done", 'TagThread',
                          lock_print, logger_type='warning', logger_name=self.ports_and_guis.my_logger.logger.name)
            self.did_closure_fn_run = True

    # TODO, MAYBE ONE FUNCTION OR OFFLINE AND YIELD?
    def update_run_data(self, run_data_path, run_data, res=None, save_to_csv=True):
        if res is not None:
            run_data['total_run_tested'] += 1
            run_data['total_run_passed_offline'] += res.get_total_test_status()
            run_data['run_responsive_tags_yield'] = \
                (run_data['total_run_responding_tags'] / run_data['total_run_tested']) * 100
            run_data['run_offline_yield'] = \
                (run_data['total_run_passed_offline'] / run_data['total_run_tested']) * 100

        if save_to_csv:
            dict_to_csv(dict_in=run_data, path=run_data_path)

    def update_packet_data(self, packets_data_path, res=None, test_data=None, only_titles=False):

        def save_default_packet_data(summary=None):
            default_data = {'raw_packet': None, 'adv_address': None, 'decrypted_packet_type': None,
                            'group_id': None, 'flow_ver': None,
                            'test_mode': None, 'en': None, 'type': None, 'data_uid': None, 'nonce': None,
                            'enc_uid': None, 'mic': None, 'enc_payload': None, 'gw_packet': None, 'rssi': None,
                            'stat_param': None, 'time_from_start': None, 'counter_tag': None,
                            'is_valid_tag_packet': None, 'common_run_name': test_data['common_run_name'],
                            'tag_run_location': test_data['tag_run_location'],
                            'tag_reel_location': test_data['tag_reel_location'],
                            'total_test_duration': test_data['total_test_duration'],
                            'total_location_duration': test_data['total_location_duration'],
                            'status_offline': test_data['status_offline'],
                            'fail_bin': test_data['fail_bin'], 'fail_bin_str': test_data['fail_bin_str'],
                            'external_id': None,
                            'label_validated_at_loc': test_data['label_validated_at_loc'], 'test_num': test_data['test_num'],
                            'trigger_time': test_data['trigger_time'], 'packet_status': None,
                            'temperature_sensor': float(-1)}
            if summary is None:
                default_sum = {'is_test_pass': None, 'selected_tag': None, 'test_start_time': None,
                               'test_end_time': None, 'test_status': None, 'rx_channel': None,
                               'energizing_pattern': None, 'time_profile': None, 'num_packets': 0,
                               'num_cycles': 0, 'sprinkler_counter_mean': None, 'sprinkler_counter_std': None,
                               'sprinkler_counter_min': None, 'sprinkler_counter_max': None, 'tbp_mean': None,
                               'tbp_std': None, 'tbp_min': None, 'tbp_max': None, 'tbp_num_vals': None,
                               'per_mean': None, 'per_std': None, 'rssi_mean': None, 'rssi_std': None,
                               'rssi_min': None, 'rssi_max': None, 'ttfp': None, 'rx_rate_normalized': None,
                               'rx_rate': None}
            else:
                default_sum = summary

            default_packet_att = {'is_valid_packet': None, 'inlay_type': None}
            default_dict = {**default_data, **default_sum, **default_packet_att}
            default_ordered_dict = {k: default_dict[k] for k in self.packet_headers_default}
            dict_to_csv(dict_in=default_ordered_dict, path=packets_data_path, append=(not only_titles),
                        only_titles=only_titles)

        if res is not None:
            test_data['status_offline'] = int(res.get_total_test_status())
            if test_data['status_offline'] == 0:
                test_data['external_id'] = ''
            test_data['total_test_duration'] = res.get_total_test_duration()
            test_data['fail_bin'] = res.get_total_fail_bin()
            test_data['fail_bin_str'] = res.get_total_fail_bin(as_name=True)
            test_data['trigger_time'] = res.get_trigger_time()
            for i, r in enumerate(res):
                test_data['test_num'] = i
                r_sum = r.get_summary()

                # add packets info:
                if r.all_packets.size():
                    # we received packets
                    for p in r.all_packets:
                        p.add_custom_data(
                            custom_data={**test_data, **r_sum})
                    r.all_packets.to_csv(path=packets_data_path, append=True, export_packet_id=False,
                                         columns=self.packet_headers_default)
                else:
                    # no responds in current test
                    save_default_packet_data(summary=r_sum)

        else:
            test_data['test_num'] = 0
            save_default_packet_data()

    def run_data_init(self):
        global run_start_time, common_run_name, tested
        if self.value['toPrint'] == 'Yes':

            self.init_external_id = self.printing_value['firstPrintingValue']
            self.string_before_counter = self.printing_value['stringBeforeCounter']
            printing_format = self.ports_and_guis.Tag_Value['printingFormat']
            print_pass_job_name = self.printing_value['passJobName']
            self.printed_external_id, is_ok = get_printed_value(string_before_the_counter=self.string_before_counter,
                                                                digits_in_counter=4,
                                                                first_counter=self.init_external_id,
                                                                printing_format=printing_format)

        else:
            self.init_external_id = '0000'
            self.init_counter = '0000'
            self.string_before_counter = ''
            self.printed_external_id = ''
            printing_format = 'TEST'
            print_pass_job_name = ''
        # self.printed_external_id = self.first_externalID

        self.run_data = {'common_run_name': common_run_name,
                         'tester_station_name': self.ports_and_guis.tag_tester_station_name,
                         'operator': self.ports_and_guis.Tag_Value['operator'], 'reel_run_start_time': run_start_time_,
                         'reel_run_end_time': None,
                         'batch_name': self.ports_and_guis.Tag_Value['batchName'],
                         'tester_type': TesterName.OFFLINE.value,
                         'comments': self.ports_and_guis.Tag_Value['comments'],
                         'total_run_tested': 0, 'total_run_responding_tags': 0,
                         'total_run_passed_offline': 0,
                         'total_missing_labels': 0, 'run_responsive_tags_yield': float('nan'),
                         'run_offline_yield': float('nan'),
                         'conversion_type': ConversionTypes(self.ports_and_guis.Tag_Value['conversion']).name,
                         'inlay': InlayTypes(self.ports_and_guis.Tag_Value['inlay']).name,
                         'test_suite': self.ports_and_guis.Tag_Value['inlayType'],
                         'test_suite_dict': self.ports_and_guis.tests_suite,
                         'surface': SurfaceTypes(self.ports_and_guis.Tag_Value['surface']).name,
                         'to_print': self.ports_and_guis.Tag_Value['toPrint'],
                         'qr_validation': self.ports_and_guis.Tag_Value['QRRead'],
                         'qr_offset': self.ports_and_guis.Tag_Value['QRoffset'],
                         'print_pass_job_name': print_pass_job_name, 'printing_format': printing_format,
                         'external_id_prefix': self.string_before_counter,
                         'external_id_suffix_init_value': self.init_external_id,
                         'coupler_partnumber': '',
                         'gw_version': self.ports_and_guis.ver, 'py_wiliot_version': get_version(), 'upload_date': None,
                         'owner_id': 'wiliot-ops', 'temperature_sensor_enable': self.ports_and_guis.temperature_enabled,
                         'ttfp_avg': float('nan')}

        self.test_data = {'common_run_name': common_run_name, 'tag_run_location': tested,
                          'total_location_duration': None, 'total_test_duration': None,
                          'status_offline': False, 'fail_bin': FailureCodes.NONE.value,
                          'fail_bin_str': FailureCodes.NONE.name,
                          'external_id': self.printed_external_id,
                          'label_validated_at_loc': self.events.qr_val.is_set(), 'trigger_time': None,
                          'test_num': 0, 'temperature_sensor': float(-1), 'tag_reel_location': self.tag_reel_location}


class R2RThread(threading.Thread):
    """
    Thread that controls R2R machine

    Parameters:
        @type events: class MainEvents (costume made class that has all of the Events of the program threads)
        @param events: has all of the Events of the program threads
        @type ports_and_guis: class PortsAndGuis (costume made class that has all of the ports and gui inputs for the
              program threads)
        @param ports_and_guis: has all of the ports and gui inputs for the program threads

    Exceptions:

    @except Exception: 'r2r_thread got an Exception, press Continue or Stop'
            exception details will be printed
            Exception might be either:
                1. Send GPIO pulse failed
                2. GPIO pulse was sent twice

    Events:
        listen/ waits on:
        events.done_or_stop => event that equals to (events.done_to_r2r_thread OR events.stop_to_r2r_thread)
        events.done_to_r2r_thread => kills R2R thread main loop if set
        events.pass_to_r2r_thread => notify if current tag passed. if set, send pulse on "Pass" GPIO line
        events.fail_to_r2r_thread => notify if current tag failed. if set, send pulse on "Fail" GPIO line
        events.start_to_r2r_thread => enable/disable R2R movement. Sends pulse on "Start/Stop machine" GPIO line
        events.enable_missing_label_to_r2r_thread => notify if missing label mode is enabled
            (skips current tag location in case of missing label up to maxMissingLabels set by user)


        sets:
        events.r2r_ready => notify if R2R in ready for movement
        events.stop_to_r2r_thread => stops the R2R from running in case of end of run or exception

    Logging:
        the logging from this thread will be to logging.debug()
        """

    def __init__(self, events, ports_and_guis, no_gui=False):
        """
        Initialize Constants
        """
        super(R2RThread, self).__init__(daemon=True)
        self.exception_queue = Queue()
        self.events = events
        self.done_or_stop = or_event_set(self.events.done_to_r2r_thread, self.events.stop_to_r2r_thread)
        self.r2r_events_or = or_event_set(self.events.pass_to_r2r_thread, self.events.fail_to_r2r_thread,
                                          self.events.start_to_r2r_thread, self.done_or_stop,
                                          self.events.enable_missing_label_to_r2r_thread,
                                          self.events.stop_to_test_r2r_thread,
                                          self.events.start_to_test_r2r_thread)
        self.en_missing_label = False
        self.ports_and_guis = ports_and_guis
        self.offset = int(self.ports_and_guis.Tag_Value['printOffset'])
        self.printing_queue = Queue(maxsize=100)
        for ind in range(self.offset):
            self.printing_queue.put(2)  # fail GPIO pulse

        self.my_gpio = self.ports_and_guis.R2R_myGPIO
        self.no_gui = no_gui

    @pyqtSlot()
    def run(self):
        """
        runs the thread
        """
        die = False
        while not die:
            time.sleep(0)
            try:
                self.r2r_events_or.wait()
                if self.done_or_stop.is_set():
                    self.my_gpio.gpio_state(3, "OFF")
                    msg = "PC send stop to R2R"
                    printing_func(msg, 'R2RThread', lock_print, logger_type='info',
                                  logger_name=self.ports_and_guis.my_logger.logger.name)
                    self.events.stop_to_r2r_thread.clear()
                    if self.no_gui:
                        self.events.stop_main_trigger.set()
                    if self.events.done_to_r2r_thread.isSet():
                        self.ports_and_guis.my_logger.logger.warning('R2RThread recieved - Job is done')
                        die = True

                if self.events.start_to_r2r_thread.is_set():
                    if self.en_missing_label:
                        msg = "PC send stop + start + fail to R2R"
                        printing_func(msg, 'R2RThread', lock_print, logger_type='info',
                                      logger_name=self.ports_and_guis.my_logger.logger.name)
                        self.my_gpio.gpio_state(3, "OFF")
                    else:
                        msg = "PC send start + fail to R2R"
                        printing_func(msg, 'R2RThread', lock_print, logger_type='info',
                                      logger_name=self.ports_and_guis.my_logger.logger.name)
                    self.my_gpio.gpio_state(3, "ON")
                    self.printing_queue.put(2)  # fail GPIO pulse
                    self.my_gpio.pulse(self.printing_queue.get(), 50)
                    self.events.r2r_ready.set()
                    self.events.start_to_r2r_thread.clear()

                if self.events.pass_to_r2r_thread.is_set():
                    msg = "^^^^^^^^^^^^^^^^^^ PC send pass to R2R ^^^^^^^^^^^^^^^^^^"
                    printing_func(msg, 'R2RThread', lock_print, logger_type='info',
                                  logger_name=self.ports_and_guis.my_logger.results_logger.name)
                    self.printing_queue.put(1)  # pass GPIO pulse
                    self.my_gpio.pulse(self.printing_queue.get(), 50)
                    self.events.pass_to_r2r_thread.clear()
                    self.events.r2r_ready.set()

                if self.events.fail_to_r2r_thread.is_set():
                    msg = "PC send fail to R2R"
                    printing_func(msg, 'R2RThread', lock_print, logger_type='info',
                                  logger_name=self.ports_and_guis.my_logger.results_logger.name)
                    self.printing_queue.put(2)  # fail GPIO pulse
                    self.my_gpio.pulse(self.printing_queue.get(), 50)
                    self.events.fail_to_r2r_thread.clear()
                    self.events.r2r_ready.set()

                if self.events.stop_to_test_r2r_thread.is_set():
                    msg = "PC send stop to R2R"
                    printing_func(msg, 'R2RThread', lock_print, logger_type='info',
                                  logger_name=self.ports_and_guis.my_logger.logger.name)
                    self.my_gpio.gpio_state(3, "OFF")
                    self.events.stop_to_test_r2r_thread.clear()

                if self.events.start_to_test_r2r_thread.is_set():
                    msg = "PC send start to R2R"
                    printing_func(msg, 'R2RThread', lock_print, logger_type='info',
                                  logger_name=self.ports_and_guis.my_logger.logger.name)
                    self.my_gpio.gpio_state(3, "ON")
                    self.events.start_to_test_r2r_thread.clear()

                if self.events.enable_missing_label_to_r2r_thread.is_set():
                    msg = "PC send 'enable missing label' to R2R"
                    printing_func(msg, 'R2RThread', lock_print, logger_type='info',
                                  logger_name=self.ports_and_guis.my_logger.results_logger.name)
                    self.my_gpio.gpio_state(4, "ON")
                    self.events.enable_missing_label_to_r2r_thread.clear()
                    self.en_missing_label = True
                if self.events.disable_missing_label_to_r2r_thread.is_set():
                    msg = "PC send 'disable missing label' to R2R"
                    printing_func(msg, 'R2RThread', lock_print, logger_type='info',
                                  logger_name=self.ports_and_guis.my_logger.results_logger.name)
                    self.my_gpio.gpio_state(4, "OFF")
                    self.events.disable_missing_label_to_r2r_thread.clear()
                    self.en_missing_label = False
            except Exception:
                exception_details = sys.exc_info()
                self.exception_queue.put(exception_details)
                self.events.stop_to_r2r_thread.set()  # to avoid from the run to continue printing in this case


class MainEvents:
    """
    Contains events that connect between all threads
    Events are set or cleared by threads
    Events are divided to four primary groups:
        1. TagThread events
        2. MainWindow events
        3. R2R (reel to reel machine) events
        4. Printer events

    Parameters: None
    Exceptions: None
    Events: None
    Logging: None
    """

    def __init__(self):
        """
        Initialize the events for the entire run
        """

        # set by tag_checker
        self.pass_to_r2r_thread = threading.Event()
        self.fail_to_r2r_thread = threading.Event()
        self.stop_to_test_r2r_thread = threading.Event()
        self.start_to_test_r2r_thread = threading.Event()
        # set by main
        self.start_to_r2r_thread = threading.Event()
        self.stop_to_r2r_thread = threading.Event()
        self.stop_main_trigger = threading.Event()
        # only to be sure we initialize the counters to the printer counter
        self.enable_missing_label_to_r2r_thread = threading.Event()
        self.disable_missing_label_to_r2r_thread = threading.Event()
        self.done_to_tag_thread = threading.Event()
        self.done_to_printer_thread = threading.Event()
        self.done2r2r_ready = threading.Event()
        self.done_to_r2r_thread = threading.Event()
        self.tag_thread_is_ready_to_main = threading.Event()

        # set by r2r
        # both printer and tag thread will wait on it. only printer will .clear() it (in printing mode)
        self.r2r_ready = threading.Event()
        # start qr read_out
        self.qr_queue = Queue()
        self.tag_status_queue = Queue()
        self.start_compare = threading.Event()
        self.qr_read_success = threading.Event()
        self.qr_val = threading.Event()
        # printer events
        self.was_pass_to_printer = threading.Event()
        self.was_fail_to_printer = threading.Event()
        self.printer_success = threading.Event()
        self.printer_error = threading.Event()
        self.printer_event = or_event_set(self.printer_success, self.printer_error)
        self.printer_validation_success = threading.Event()
        # being used in printer thread too
        self.r2r_ready_or_done2tag = or_event_set(self.r2r_ready, self.done2r2r_ready)
        self.validation_success = or_event_set(self.printer_validation_success, self.qr_read_success)


class PortsAndGuis:
    """
    class which is responsible for initializing peripheral's ports and get data from run GUIs

    Parameters: None
    Exceptions: None
    Events: None
    Logging: None
    """

    def __init__(self, test_config_path=None):
        """
        Initialize the runs ports and gets data from the guis
        """
        if test_config_path is None:
            self.no_gui = False
            self.test_config_path = ''
        else:
            self.no_gui = True
            self.test_config_path = test_config_path
        app_dir = os.path.abspath(os.path.dirname(__file__))
        self.dir_config = join(app_dir, 'configs')
        self.tests_suites_configs_path = join(self.dir_config, 'tests_suites.json')
        tests_suites_eng_path = join(self.dir_config, 'tests_suites_eng.json')
        if os.path.isfile(tests_suites_eng_path):
            self.tests_suites_configs_path = tests_suites_eng_path
        # Get tests:
        with open(self.tests_suites_configs_path, 'r') as f:
            self.all_tests_suites = json.load(f)

        # run values (1st GUI)
        if self.no_gui:
            if os.path.isfile(path=test_config_path):
                with open(self.test_config_path, 'r') as f:
                    self.Tag_Value = json.load(f)
            else:
                raise Exception('test_config_path does not exist')
        else:
            self.Tag_Value = open_session(inlay_type_list=list(self.all_tests_suites.keys()))
        # Getting the config values
        self.init_config_values()
        self.tests_suite = self.all_tests_suites[self.Tag_Value['inlayType']]
        self.total_time = 0
        for stage in self.tests_suite['tests']:
            if 'maxTime' in stage.keys():
                self.total_time += stage['maxTime']
            if 'delayBeforeNextTest' in stage.keys():
                self.total_time += stage['delayBeforeNextTest']
            if 'DelayAfterTest' in stage.keys():
                self.total_time += stage['DelayAfterTest']
        # for Tag thread ###########
        # check if production mode or test mode to set environment for cloud_api
        env = self.Tag_Value['Environment']
        owner_id = self.Tag_Value['OwnerId']
        if 'prod' in env:
            self.env = ''
        elif 'test' in env:
            self.env = '/test'
        else:
            raise Exception('environment can be production or test only (got {})'.format(env))

        print('Starting run in {} mode'.format(str(self.env)))
        # printing values (2nd GUI)
        self.print_test = False
        if self.Tag_Value['toPrint'] == 'Yes':
            self.to_print = True
            if self.Tag_Value['printingFormat'] == 'Test':
                self.print_test = True
                self.Tag_Printing_Value, self.Tag_is_OK = printing_test_window()
                if not self.Tag_is_OK:
                    msg = 'Impossible printing values entered by the user, the program will exit now'
                    printing_func(msg, 'PortsAndGuis', lock_print, logger_type='debug',
                                  logger_name=self.my_logger.logger.name)
                    sys.exit(0)

            elif self.Tag_Value['printingFormat'] == 'SGTIN' or self.Tag_Value['printingFormat'] == 'Barcode':
                self.Tag_Printing_Value, self.Tag_is_OK = printing_sgtin_window(self.env, owner_id,
                                                                                self.Tag_Value['printingFormat'])
                if not self.Tag_is_OK:
                    msg = 'user exited the program'
                    printing_func(msg, 'PortsAndGuis', lock_print, logger_type='debug',
                                  logger_name=self.my_logger.logger.name)
                    sys.exit(0)
            else:
                msg = 'user chose unsupported printing format!!!'
                printing_func(msg, 'PortsAndGuis', lock_print, logger_type='debug',
                              logger_name=self.my_logger.logger.name)
        # path for log file

        self.env_dirs = WiliotDir()
        self.WILIOT_DIR = self.env_dirs.get_wiliot_root_app_dir()

        self.machine_dir = join(self.WILIOT_DIR, 'offline')
        self.logs_dir = join(self.machine_dir, 'logs')
        self.new_path = join(self.logs_dir, str(self.Tag_Value['batchName']))
        # new_path = 'logs/' + str(self.Tag_Value['batchName'])
        if not os.path.exists(self.new_path):
            os.makedirs(self.new_path)
        global R2R_code_version
        global run_start_time, common_run_name
        global reel_name
        reel_name = self.Tag_Value['batchName'].rstrip()
        common_run_name = reel_name + '_' + run_start_time
        self.my_logger = WiliotTesterLog(run_name=common_run_name)
        self.my_logger.set_logger(log_path=self.new_path)
        self.my_logger.create_data_dir(data_path=self.new_path, tester_name='offline',
                                       run_name=common_run_name)

        self.auto_attenuator_enable = self.Tag_Value['externalAttenuator']
        if self.auto_attenuator_enable:
            try:
                if self.Tag_Value['attnComport'].upper() == 'AUTO':
                    self.attenuator = Attenuator('API').GetActiveTE()
                else:
                    self.attenuator = Attenuator('API',
                                                 comport='COM' + str(self.Tag_Value['attnComport'])).GetActiveTE()
                current_attn = self.attenuator.Getattn()
            except Exception as e:
                raise EquipmentError('Attenuator Error - Verify Attenuator connection')

        self.config_equipment(temperature_sensor=True)

        # check if the system variable exist
        assert ('testerStationName' in os.environ), 'testerStationName is missing from PC environment variables, ' \
                                                    'please add it in the following convention:' \
                                                    ' <company name>_<tester number>'
        self.tag_tester_station_name = os.environ['testerStationName']
        # serial for GW
        self.GwObj = WiliotGateway(auto_connect=True, logger_name=self.my_logger.gw_logger.name,
                                   is_multi_processes=True, log_dir_for_multi_processes=os.path.join(self.new_path,
                                                                                                     common_run_name))
        self.ver, _ = self.GwObj.get_gw_version()

        if 'additionalGW' in self.tests_suite:
            self.energizerGW = WiliotGateway(logger_name=self.my_logger.gw_logger.name,
                                             port=self.tests_suite['additionalGW']['port'])
            if self.energizerGW.connected:
                self.energizerGW.reset_gw()
                sleep(5)
                self.energizerGW.write('!listen_to_tag_only 1')
                sleep(1)
                self.energizerGW.write('!set_tester_mode 1')
                sleep(1)
                self.energizerGW.write('!pl_gw_config 0')
                sleep(1)
                self.energizerGW.write('!sub1g_sync 1')

                try:
                    self.additional_gw_mode = DualGWMode(self.tests_suite['additionalGW']['mode'])
                except Exception as e:
                    raise Exception('no mode in additionalGW dict in test suite or invalid mode: {}'.format(e))

                self.energizerGW.config_gw(received_channel=self.tests_suite['additionalGW']['rxChannel'],
                                           energy_pattern_val=self.tests_suite['additionalGW']['energizingPattern'],
                                           time_profile_val=self.tests_suite['additionalGW']['timeProfile'],
                                           output_power_val=self.tests_suite['additionalGW']['gw_output_power'],
                                           bypass_pa_val=self.tests_suite['additionalGW']['bypass_pa'], with_ack=False,
                                           start_gw_app=False)
                if 'sub1g_power' in self.tests_suite['additionalGW']:
                    sleep(1)  # sometimes when commands sends one after another the uart failed
                    self.energizerGW.config_gw(sub1g_output_power_val=self.tests_suite['additionalGW']['sub1g_power'],
                                               start_gw_app=False)

                if 'gw_commands' in self.tests_suite['additionalGW']:
                    if len(self.tests_suite['additionalGW']['gw_commands']) > 0:
                        for command in self.tests_suite['additionalGW']['gw_commands']:
                            sleep(1)  # sometimes when commands sends one after another the uart failed
                            self.energizerGW.write(command)
                if self.additional_gw_mode == DualGWMode.STATIC:
                    sleep(1)  # sometimes when commands sends one after another the uart failed
                    self.energizerGW.write('!gateway_app')

        else:
            self.energizerGW = False



        # for Printer thread ###########
        self.Printer_socket = ''  # will only be opened by the thread
        if self.Tag_Value['printingFormat'] == 'Test':
            self.filename = 'gui_printer_inputs_4_Test_do_not_delete.json'
        elif self.Tag_Value['printingFormat'] == 'SGTIN' or self.Tag_Value['printingFormat'] == 'Barcode':
            self.filename = 'gui_printer_inputs_4_SGTIN_do_not_delete.json'

        else:
            msg = 'The print Job Name inserted is not supported at the moment, You will need to press Stop'
            printing_func(msg, 'PortsAndGuis', lock_print, logger_type='debug', logger_name=self.my_logger.logger.name)

        # check printing configs and save it locally
        self.folder_path = 'configs'
        self.data_for_printing = open_json(folder_path=self.folder_path,
                                           file_path=os.path.join(self.folder_path, self.filename),
                                           default_values=DefaultGUIValues(
                                               self.Tag_Value['printingFormat']).default_gui_values)
        # for R2R thread ###########
        self.R2R_myGPIO = R2rGpio()

    def open_printer_socket(self):
        """
        opens the printer socket
        """
        self.Printer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Printer_socket.settimeout(PRINTER_SOCKET_TIMEOUT)
        self.Printer_socket.connect((self.configs_for_printer_values['TCP_IP'],
                                     int(self.configs_for_printer_values['TCP_PORT'])))

    def update_printer_gui_inputs(self):
        """
        save the last pass value for crash support.
        passed global variable will be updated at tag Thread and should be correct here
        """
        self.data_for_printing['firstPrintingValue'] = str(int(self.data_for_printing['firstPrintingValue']) + 1)
        file_path = os.path.join('configs', self.filename)
        json.dump(self.data_for_printing, open(file_path, "w"))

    def init_config_values(self):
        """
        initialize the config values for the run
        """

        config_defaults = ConfigDefaults()

        self.configs_for_printer_file_values_path = self.dir_config + '/configs_for_printer_values.json'
        self.configs_for_printer_values = open_json(self.dir_config, self.configs_for_printer_file_values_path,
                                                    config_defaults.get_printer_defaults())

    def config_attenuator(self):
        """
        configs attenuator for this run
        :Return: True if configuration found and attenuator was configured successfully, False otherwise
        """
        if not self.auto_attenuator_enable:
            msg = "according to configs.test_configs (AutoAttenuatorEnable) automatic attenuator is not connected, " \
                  "or should not be used."
            printing_func(str_to_print=msg, logging_entity='PortsAndGuis', lock_print=lock_print,
                          do_log=True, logger_type='debug', logger_name=self.my_logger.logger.name)
            try:
                attn = set_calibration_attn(set_optimal_attn=False)
                if attn is None:
                    msg = "failed to set attenuation"
                else:
                    msg = 'Attenuation is set (' + str(attn) + "dB)"
            except EquipmentError:
                msg = 'was not able to open port to Attenuator, will continue this run without attenuator configuration'

            except Exception:
                msg = 'was not able to open json with attenuator config data, will continue this run without ' \
                      'attenuator configuration'
        else:
            try:
                tmp_path = ('configs/test_configs.json')
                attn = set_calibration_attn(set_optimal_attn=True, config_path=tmp_path)
                if attn is None:
                    msg = "failed to set attenuation, you will need to press Stop"
                    printing_func(str_to_print=msg, logging_entity='PortsAndGuis', lock_print=lock_print,
                                  do_log=True, logger_type='debug', logger_name=self.my_logger.logger.name)
                    raise Exception("AutoAttenuatorEnable=Yes but failed to set attenuation")
                else:
                    msg = 'Attenuation is set (' + str(attn) + "dB)"
            except EquipmentError:
                msg = 'was not able to open port to Attenuator, you will need to press Stop\n' \
                      'if you want to restart run without using auto attenuator please change the field ' \
                      '"AutoAttenuatorEnable" in configs.test_config.json to "No"'
                printing_func(str_to_print=msg, logging_entity='PortsAndGuis', lock_print=lock_print,
                              do_log=True, logger_type='debug', logger_name=self.my_logger.logger.name)
                raise Exception("AutoAttenuatorEnable=Yes but could not open port to Attenuator")
            except Exception:
                msg = 'was not able to open json with attenuator config data, will continue this run without ' \
                      'attenuator configuration'

        printing_func(str_to_print=msg, logging_entity='PortsAndGuis', lock_print=lock_print,
                      do_log=True, logger_type='debug', logger_name=self.my_logger.logger.name)

    def config_equipment(self, temperature_sensor=True):
        """
        :type temperature_sensor: bool
        :param temperature_sensor: if True will config temperature sensor
        :type attenuator: bool
        :param attenuator: if True will config attenuator
        configs equipment that needed for the run
        """
        # temperature sensor and auto attenuator
        global temperature_sensor_enable
        temperature_sensor_enable = False
        wiliot_folder_path = user_data_dir('offline', 'wiliot')
        folder_path = join(wiliot_folder_path, 'configs')
        # folder_path = 'configs'
        cfg_file_name = 'test_configs.json'
        # if file or folder doesn't exist will create json file with temperatureSensorEnable = 'No' and raise exception
        if os.path.isdir(folder_path):
            file_path = os.path.join(folder_path, cfg_file_name)
            if os.path.exists(file_path):
                self.test_configs = open_json(folder_path=folder_path,
                                              file_path=os.path.join(folder_path, cfg_file_name))
            else:
                msg = "Config file doesn't exist\n Creating test_config.json"
                printing_func(msg, 'PortsAndGuis', lock_print, logger_type='debug',
                              logger_name=self.my_logger.logger.name)
                with open(file_path, 'w') as cfg:
                    json.dump({"temperatureSensorEnable": "No",
                               "AutoAttenuatorEnable": str(self.auto_attenuator_enable)}, cfg)
                # raise Exception('test_config.json was created\n Temperature sensor is disabled\n'
                #                 'You will need to press Stop')
                msg = 'test_config.json was created\n Temperature sensor is disabled\nYou will need to press Stop'
                printing_func(msg, 'PortsAndGuis', lock_print, logger_type='info',
                              logger_name=self.my_logger.logger.name)

                self.test_configs = open_json(folder_path=folder_path,
                                              file_path=file_path)
        else:
            msg = "'configs' directory doesn't exist\n Creating directory and test_config.json"
            printing_func(msg, 'PortsAndGuis', lock_print, logger_type='debug', logger_name=self.my_logger.logger.name)
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path, cfg_file_name)
            with open(file_path, 'w') as cfg:
                if self.auto_attenuator_enable:
                    json.dump({"temperatureSensorEnable": "No", "AutoAttenuatorEnable": "Yes"}, cfg)
                else:
                    json.dump({"temperatureSensorEnable": "No", "AutoAttenuatorEnable": "No"}, cfg)
            # raise Exception('test_config.json was created\n Temperature sensor and Auto Attenuator is disabled\n'
            #                 'You will need to press Stop')
            msg = 'test_config.json was created\n Temperature sensor and Auto Attenuator is disabled\n' \
                  'You will need to press Stop'
            printing_func(msg, 'PortsAndGuis', lock_print, logger_type='info', logger_name=self.my_logger.logger.name)

            self.test_configs = open_json(folder_path=folder_path,
                                          file_path=file_path)

        if temperature_sensor:
            if 'temperatureSensorEnable' not in self.test_configs.keys() or \
                    'AutoAttenuatorEnable' not in self.test_configs.keys():
                with open(file_path, 'w') as cfg:
                    if self.auto_attenuator_enable:
                        json.dump({"temperatureSensorEnable": "No", "AutoAttenuatorEnable": "Yes"}, cfg)
                    else:
                        json.dump({"temperatureSensorEnable": "No", "AutoAttenuatorEnable": "No"}, cfg)
                raise Exception('test_config.json missing some values, will return it to default values\n'
                                'You will need to press Stop')
            if self.test_configs['temperatureSensorEnable'].upper() == 'NO':
                temperature_sensor_enable = False
                self.temperature_enabled = False
            elif self.test_configs['temperatureSensorEnable'].upper() == 'YES':
                temperature_sensor_enable = True
                self.temperature_enabled = True
            else:  # illegal inputs will be ignored
                raise Exception("Valid values for temperatureSensorEnable are 'Yes' or 'No'\n "
                                "You will need to press Stop")
            if temperature_sensor_enable:
                self.Tag_t = set_temperature()
            else:
                self.Tag_t = None
        else:
            self.temperature_enabled = False
            self.Tag_t = None

        # if attenuator:
        #     self.my_logger.logger.info('External attenuator enabled')
        #     self.config_attenuator()


class ConsolePanelHandler_GUI(logging.Handler):

    def __init__(self, sig):
        # super().__init__()
        logging.Handler.__init__(self)
        # logging.StreamHandler.__init__(self, stream)
        self.stream = sig

    def handle(self, record):
        rv = self.filter(record)
        if rv:
            self.acquire()
            try:
                self.emit(record)
            finally:
                self.release()
        return rv

    def emit(self, record):
        try:
            self.stream.emit(self.format(record))
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)


class MainWindow(QMainWindow):
    """
    Thread that opens and controls the GUI, opens all threads, sets/clears timers for all threads and handles exceptions
    This class will call for upload to cloud

    Parameters:
        values set by user in Offline Tester GUI:
            @Allow multiple missing label in row: dropdown list "Yes"/"No"
                If set to "No" the run will pause when a missing label is detected
            @Max missing labels in a row: int
                In case this number of missing label in row is reached, the run will pause
            @To print?: dropdown list "Yes"/"No"
                Enable/Disable printer. If set to "Yes" printing GUI will be opened after user pressed "Submit"
            @What is the printing job format?: dropdown list "SGTIN"/"Test"
            @Reel_name: str
            @Tags Generation: dropdown list with tags generation (e.g. "D2")
            @Inlay type: dropdown list with inlay types (e.g. "Dual Band")
            @Inlay serial number (3 digits): serial number for given inlay type
            @Desired amount of tags (will stop the run after this amount of tags): int.
                The run will pause after the amount written is reached. The user can choose to stop the run or continue.
            @Desired amount of pass (will stop the run after this amount of passes): int
                The run will pause after the amount written is reached in tags that passed.
                The user can choose to stop the run or continue.
            @Surface: dropdown list with various testing surfaces with given dielectric constant (Er)
            @Is converted?: dropdown list "Yes"/"No"  => if tag is converted or not
            @comments: text box for user comments

    Exceptions:
        @except Exception: exception occurred in one of the threads => calls look_for_exceptions()
            look_for_exceptions() will call handle_r2r_exception() which prints and handles the exception if possible

    Events:
        listen/ waits on:
            events.tag_thread_is_ready_to_main => event from TagThread. if set, TagThread is ready
            events.printer_event => wait for response from printer (printer_success or printer_error)
            events.printer_success => the last print was successful
            events.r2r_ready => notify if R2R in ready for movement

        sets:
            events.start_to_r2r_thread => enable/disable R2R movement. Sends pulse on "Start/Stop machine" GPIO line
            events.stop_to_r2r_thread => stops the R2R from running in case of end of run or exception
            events.done_to_tag_thread => closes TagThread at the end of the run
            events.done2r2r_ready => closes R2RThread
            events.done_to_r2r_thread => kills R2R thread main loop if set
            events.done_to_printer_thread => user pressed Stop (end the program) - to avoid deadlock


    Logging:
        logging to logging.debug() and logging.info()
    """
    sig = pyqtSignal(str)

    def __init__(self, test_config_path=None):
        """
        Initialize the runs threads and classes
        """
        try:
            super(MainWindow, self).__init__()
            self.test_config_path = test_config_path
            if test_config_path is None:
                self.no_gui = False
            else:
                self.no_gui = True
                print('no gui. using {}'.format(self.test_config_path))
            self.init_ok = True
            self.events = MainEvents()
            self.passed_every_50 = []
            self.last_tested_num = 0
            self.final_close = False
            self.last_passed_num = 0
            self.yield_over_time = []
            self.calculate_interval = 10
            self.to_print = False
            self.printer = None
            self.update_timer = None
            self.exception_message = None
            global calculate_interval
            calculate_interval = self.calculate_interval
            self.calculate_on = 50
            global calculate_on
            calculate_on = self.calculate_on
            self.first_reached_to_desired_passes = False
            self.first_reached_to_desired_tags = False
            self.yield_drop_happened = False
            self.yield_was_high_lately = True
            self.prev_y_len = 0
            self.waiting_for_user_to_press_stop_because_printer = False

            # logging.getLogger().setLevel(logging.DEBUG)
            # stream_handler = logging.StreamHandler()
            # logging.getLogger().addHandler(stream_handler)

            self.ports_and_guis = PortsAndGuis(self.test_config_path)
            self.to_scan = self.ports_and_guis.Tag_Value['QRRead']
            self.maxfail = int(self.ports_and_guis.Tag_Value['maxFailStop'])
            self.minyield = int(self.ports_and_guis.Tag_Value['maxYieldStop'])
            self.ignore_stop_conditions = self.ports_and_guis.Tag_Value['ignoreStop']
            if self.maxfail > 0:
                self.calculate_on = self.maxfail

            self.cloud_connection = True
            if self.no_gui:
                if os.path.isfile(path=self.test_config_path):
                    with open(self.test_config_path, 'r') as f:
                        gui_configs = json.load(f)
                        if 'upload_to_cloud' in gui_configs and gui_configs['upload_to_cloud'].lower() == 'no':
                            self.cloud_connection = False
            if self.cloud_connection:
                file_path, api_key, is_successful = check_user_config_is_ok(env=self.ports_and_guis.env,
                                                                            owner_id=self.ports_and_guis.Tag_Value[
                                                                                'OwnerId'])
                self.client = ManufacturingClient(api_key=api_key, env=self.ports_and_guis.env,
                                                  logger_=self.ports_and_guis.my_logger.logger.name,
                                                  log_file=self.ports_and_guis.my_logger.log_path)

            self.r2r_thread = R2RThread(self.events, self.ports_and_guis, no_gui=self.no_gui)
            self.tag_checker_thread = TagThread(self.events, self.ports_and_guis)

            if (self.printer is not None and not self.printer.exception_queue.empty()) or \
                    not self.tag_checker_thread.exception_queue.empty() or not self.r2r_thread.exception_queue.empty():
                self.events.stop_to_r2r_thread.set()
                self.handle_r2r_exception()
                self.init_ok = False

            self.events.tag_thread_is_ready_to_main.wait()
            self.events.tag_thread_is_ready_to_main.clear()

            self.pass_job_name = self.tag_checker_thread.printing_value['passJobName']  # will be set inside config
            self.to_print = self.tag_checker_thread.to_print
            self.start_value = int(self.tag_checker_thread.printing_value['firstPrintingValue'])

            # printer set-up ####################################################################
            # happens here so we will wait less until the printer will start up (will happen in the background)
            if self.to_print:
                self.printer = Printer(self.start_value, self.pass_job_name, self.events, self.ports_and_guis)
                self.look_for_exceptions()

            if self.to_scan == 'Yes':
                self.tag_comparing_qr = QRThread(self.events, self.ports_and_guis, print=self.to_print)

            self.gw_version = self.ports_and_guis.ver
            self.wiliot_ver = get_version()
            self.open_ui()  # starts recurring_timer() that starts look_for_exceptions()
            if self.init_ok:
                self.r2r_thread.start()
                self.tag_checker_thread.start()
                self.events.tag_thread_is_ready_to_main.wait()
                self.events.tag_thread_is_ready_to_main.clear()

                if self.to_print:
                    if self.to_scan == 'Yes':
                        self.tag_comparing_qr.start()

                    else:
                        self.printer.start()
                    self.events.printer_event.wait()
                    if self.events.printer_success.isSet():
                        self.events.printer_success.clear()
                        msg = 'Printer is ready to start'
                        printing_func(msg, 'MainWindow', lock_print, logger_type='debug',
                                      logger_name=self.ports_and_guis.my_logger.logger.name)
                else:
                    if self.to_scan == 'Yes':
                        self.tag_comparing_qr.start()

                self.events.start_to_r2r_thread.set()
        except Exception:
            exception_details = sys.exc_info()
            msg = 'Exception detected during initialization:'
            try:
                printing_func(msg, 'MainWindow', lock_print, logger_type='warning',
                              logger_name=self.ports_and_guis.my_logger.logger.name)
            except Exception:
                printing_func(msg, 'MainWindow', lock_print, logger_type='warning')
            print_exception(exception_details, printing_lock=lock_print)
            self.look_for_exceptions()

        # done will be raised from stop_fn (user pressed done)

    def open_ui(self):
        """
        opens the run main GUI that will present the run data and gives to the user ability to Stop/Continue/Pause
        """
        self.stop_label = QLabel("If you want to stop this run, press stop")
        self.stop_label.setFont(QFont('SansSerif', 10))
        self.reel_label = QLabel("Reel Name: ")
        self.reel_label.setFont(QFont('SansSerif', 10))
        self.reel_label.setStyleSheet('.QLabel {padding-top: 10px; font-weight: bold; font-size: 25px; color:#ff5e5e;}')
        self.reel_label.setFont(QFont('SansSerif', 10))
        self.tested = QLabel("Tested = 0, Passed = 0, Yield = -1%")
        self.tested.setFont(QFont('SansSerif', 10))
        self.last_tag_str = QLabel("Last Tag Passed: ")
        self.last_tag_str.setFont(QFont('SansSerif', 10, weight=QFont.Bold))
        self.last_pass = QLabel("No tag has passed yet :(")
        self.last_pass.setFont(QFont('SansSerif', 10))
        layout = QVBoxLayout()

        self.stop = QPushButton("Stop")
        self.stop.setStyleSheet("background-color: #FD4B4B")
        self.stop.setFont(QFont('SansSerif', 10))
        self.stop.setFixedSize(QSize(300, 22))
        self.stop.pressed.connect(self.close)

        self.c = ConsolePanelHandler_GUI(self.sig)
        self.c.setLevel(logging.WARNING)
        self.text_box = QPlainTextEdit()
        self.text_box.setPlaceholderText("Warnings will be printed here")
        self.text_box.setMaximumBlockCount(1000)
        # self.text_box.centerOnScroll()
        self.text_box.setReadOnly(True)
        # addConsoleHandler(self.appendDebug , logging.DEBUG)
        # console_log = logging.getLogger()
        # console_log.setLevel(logging.WARNING)
        self.ports_and_guis.my_logger.logger.addHandler(self.c)
        # logging.getLogger().setLevel(logging.INFO) #Change to the wanted level of log
        self.sig.connect(self.appendDebug)
        self.text_box.moveCursor(QTextCursor.End)

        self.graphWidget = pg.PlotWidget()
        self.x = []  # 0 time points
        self.y = []  # will contain the yield over time
        self.graphWidget.setBackground('w')
        # Add Title
        self.graphWidget.setTitle("Yield over time", color=QColor("56C2FF"), size="20pt")
        styles = {"color": "#f00", "font-size": "14px"}
        self.graphWidget.setLabel("left", "Yield for the last 50 tags [%]", **styles)
        self.graphWidget.setLabel("bottom", "Last tag location [x*" + str(self.calculate_interval) + "+" +
                                  str(self.calculate_on) + "]", **styles)
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        self.versions = QLabel("PyWiliot Version: {}\nGW Version: {}".format(self.wiliot_ver, self.gw_version))
        self.versions.setFont(QFont('SansSerif', 10, weight=QFont.Bold))

        layout.addWidget(self.reel_label)
        layout.addWidget(self.stop_label)
        layout.addWidget(self.stop)
        layout.addWidget(self.last_tag_str)
        layout.addWidget(self.last_pass)
        layout.addWidget(self.tested)
        # layout.addWidget(self.debug)
        layout.addWidget(self.text_box)
        layout.addWidget(self.graphWidget)
        layout.addWidget(self.versions)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        # self.w = Error_window()
        self.show()

        # updates the GUI and stops all if exception happened
        self.update_timer = QTimer()
        self.update_timer.setInterval(500)
        self.update_timer.timeout.connect(self.recurring_timer)
        self.update_timer.start()

    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("Are you sure want to stop and exit?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            event.accept()
            if not self.final_close:
                self.stop_fn()
        else:
            event.ignore()

    @pyqtSlot(str)
    def appendDebug(self, string):
        self.text_box.appendPlainText(string)  # +'\n')

    # GUI functions ##########################################################
    def stop_fn(self):
        """
        will be triggered by the Stop button and will end the run.
        will upload run's data to cloud and close the threads.
        """
        self.final_close = True
        self.events.done_to_r2r_thread.set()
        global tested, passed, missing_labels, responded
        global last_pass_string, under_threshold, problem_in_locations_hist, fail_bin_list
        global reel_name
        if tested == 0:
            yield_ = -1.0
        else:
            if tested > 1:
                # if tested > passed:
                #     tested = tested - 1
                yield_ = passed / tested * 100
            else:
                if passed == 0:
                    yield_ = 0
                else:
                    yield_ = 100

        if self.ports_and_guis.GwObj.connected:
            self.update_timer.stop()
        # self.close()
        ttfgp_avg = None
        if len(self.tag_checker_thread.ttfgp_list) > 0:
            ttfgp_avg = mean(self.tag_checker_thread.ttfgp_list)
        self.events.done_to_tag_thread.set()
        if self.first_reached_to_desired_tags or self.first_reached_to_desired_passes:
            time.sleep(0.5)
        # check logging due to printing offset:
        if self.ports_and_guis.Tag_Value['toPrint'] == 'Yes':
            self.check_logging_due_to_printing_offset()

        self.events.done_to_printer_thread.set()
        self.events.done2r2r_ready.set()
        self.events.done_to_r2r_thread.set()
        self.events.start_compare.clear()

        if self.ports_and_guis.energizerGW:
            self.ports_and_guis.energizerGW.write('cancel')
            self.ports_and_guis.energizerGW.exit_gw_api()
        if self.r2r_thread.is_alive():
            self.r2r_thread.join()
        self.ports_and_guis.my_logger.results_logger.info('R2R Thread closed')
        if self.tag_checker_thread.is_alive():
            self.tag_checker_thread.join()
        else:
            self.ports_and_guis.my_logger.results_logger.info('Closed Tag Thread')
        try:
            self.ports_and_guis.GwObj.exit_gw_api()
            if self.auto_attenuator_enable:
                self.ports_and_guis.attenuator.close_port()
        except Exception:
            pass
        try:
            window.showMinimized()
        except Exception as e:
            print('could not minimized the window: {}'.format(e))
        values = None
        if self.exception_message is not None:
            SimGUI.popup(self.exception_message, no_titlebar=True, keep_on_top=True)
        if self.no_gui:
            if os.path.isfile(path=self.test_config_path):
                with open(self.test_config_path, 'r') as f:
                    gui_configs = json.load(f)
                    if 'upload_to_cloud' in gui_configs:
                        values = {'upload': gui_configs['upload_to_cloud'], 'comments': ''}
        if values is None:
            if problem_in_locations_hist is not None:
                for k in problem_in_locations_hist.keys():
                    problem_in_locations_hist[k] = len([f for f in fail_bin_list if f == k])
            values = save_screen(tested=tested, passed=passed, yield_=yield_, missing_labels=missing_labels,
                                 problem_in_locations_hist_val=problem_in_locations_hist, ttfgp_avg=ttfgp_avg)

        # save last printed value, also being done after every pass by the printer thread (for crash support):
        env_dirs = WiliotDir()
        WILIOT_DIR = env_dirs.get_wiliot_root_app_dir()
        machine_dir = join(WILIOT_DIR, 'offline')
        local_config_dir = join(machine_dir, 'configs')

        if self.to_print:
            self.events.done_to_printer_thread.set()
            printing_format = self.ports_and_guis.Tag_Value['printingFormat']
            if printing_format == 'Test':
                filename = 'gui_printer_inputs_4_Test_do_not_delete.json'
            else:
                filename = 'gui_printer_inputs_4_SGTIN_do_not_delete.json'

            app_dir = os.path.abspath(os.path.dirname(__file__))
            self.folder_path = join(app_dir, 'configs')
            data = open_json(folder_path=self.folder_path, file_path=os.path.join(self.folder_path, filename),
                             default_values=DefaultGUIValues(printing_format).default_gui_values)
            last_printing_value = last_pass_string.split()
            if passed > 0:
                data['firstPrintingValue'] = str(int(self.tag_checker_thread.externalId))
                data['tagLocation'] = str(int(self.tag_checker_thread.tag_location))
                data['tag_reel_location'] = str(int(self.tag_checker_thread.test_data['tag_reel_location']))
            f = open(os.path.join(self.folder_path, filename), "w")
            json.dump(data, f)
            f.close()

            if self.to_print:
                if self.ports_and_guis.Tag_Value['QRRead'] != 'Yes':
                    self.printer.closure()
                    if self.printer.is_alive():
                        self.printer.join()
                    self.ports_and_guis.my_logger.results_logger.debug('Closed Printer Thread')
                else:
                    if self.tag_comparing_qr.is_alive():
                        self.tag_comparing_qr.join()
                    self.printer.closure()
                    self.ports_and_guis.my_logger.results_logger.debug('Closed QR Thread')

        res = None
        if values['upload'] == 'Yes':
            if tested > 0:
                try:
                    res = upload_to_cloud_api(batch_name=reel_name, tester_type='offline-test',
                                              run_data_csv_name=self.ports_and_guis.my_logger.run_data_path,
                                              packets_data_csv_name=self.ports_and_guis.my_logger.packets_data_path,
                                              env=self.ports_and_guis.env,
                                              owner_id=self.ports_and_guis.Tag_Value['OwnerId'],
                                              logger_=self.ports_and_guis.my_logger.gw_logger.name, is_path=True,
                                              client=self.client)
                    sleep(2)
                except Exception:
                    exception_details = sys.exc_info()
                    print_exception(exception_details=exception_details, printing_lock=lock_print)
                    res = False

                if not res:
                    SimGUI.popup_ok("Run upload failed. Check exception error at the console and check Internet connection is available and upload logs manually",
                                    title='Upload Error',
                                    font='Calibri',
                                    keep_on_top=True,
                                    auto_close=False,
                                    no_titlebar=True)

            else:
                self.ports_and_guis.my_logger.results_logger.warning(
                    'tested value is incorrect, please check run_data file')
                res = False

            if not res:
                msg = 'Upload to cloud failed!!!!!!!!!\ngot an error while uploading to cloud'
                printing_func(msg, 'MainWindow', lock_print, logger_type='warning',
                              logger_name=self.ports_and_guis.my_logger.results_logger.name)
            else:
                self.ports_and_guis.my_logger.results_logger.info('Uploaded to cloud ' + str(res))
        else:
            self.ports_and_guis.my_logger.results_logger.info('Uploaded to cloud? No')

        if res is not None and not self.no_gui:
            upload_conclusion(failed_tags=None, succeeded_csv_uploads=res)
        try:
            try:
                responded_yield = (responded * 100)/tested
            except Exception:
                responded_yield = -1
            msg = "Stopped by the operator.\n" + 'Reels yield_over_time is: |' + str(self.yield_over_time) + \
                  '| interval: |' + str(self.calculate_interval) + '|, on: |' + str(self.calculate_on) + \
                  '\nLast words: ' + values['comments'] + '\nTested = ' + str(tested) + ', Passed = ' + str(passed) + \
                  'Responded Yield = ' + str(responded_yield) + '%, Yield = ' + str(yield_) + '%' + ', Missing labels = ' + str(missing_labels)
            printing_func(msg, 'MainWindow', lock_print, logger_type='info',
                          logger_name=self.ports_and_guis.my_logger.results_logger.name)
        except Exception:
            self.ports_and_guis.my_logger.results_logger.warning('User finished the run from GUI')
        try:
            self.ports_and_guis.GwObj.exit_gw_api()
        except:
            pass  # some other thread close the gw app

        self.ports_and_guis.my_logger.results_logger.info('Run finished')
        # window.close()
        self.ports_and_guis.R2R_myGPIO.__del__()
        time.sleep(1)
        sys.exit(0)

    def recurring_timer(self):
        """
        update the runs main GUI, checks that the other threads are OK (no exceptions)
        """
        global tested, passed, missing_labels, black_list_size, responded
        global last_pass_string, reel_name

        if tested == 0:
            yield_ = -1.0
            responded_yield = -1
            self.reel_label.setText("Reel Name: " + reel_name)
        else:
            yield_ = passed / tested * 100
            responded_yield = responded/tested*100
        self.tested.setText('Tested = ' + str(tested) + ', Passed = ' + str(passed) + ', Responded Yield = ' + str(responded_yield) + '%, Yield = ' +
                            '{0:.4g}'.format(yield_) + '%' + '\nMissing labels = ' + str(missing_labels) +
                            ', black list size = ' + str(black_list_size))
        self.last_pass.setText(last_pass_string)
        # update the graph, if there was change in the tested amount
        # because passed and tested are been updated in different times
        # we will check the passed of the prev tag => tested -1
        if tested > self.last_tested_num:
            if self.calculate_on >= tested > self.last_tested_num:
                if passed - self.last_passed_num > 0:
                    self.passed_every_50.append(1)
                else:
                    self.passed_every_50.append(0)
            elif tested > 0:
                del self.passed_every_50[0]
                if passed - self.last_passed_num > 0:
                    self.passed_every_50.append(1)
                else:
                    self.passed_every_50.append(0)

            if len(self.passed_every_50) > self.calculate_on:
                msg = 'self.passed_every_50 length is too long (self.passed_every_50 = ' + \
                      str(self.passed_every_50) + ')'
                printing_func(msg, 'MainWindow', lock_print, logger_type='warning',
                              logger_name=self.ports_and_guis.my_logger.logger.name)

            if tested % self.calculate_interval == 1 and tested > self.calculate_on:
                self.y.append(sum(self.passed_every_50) / self.calculate_on * 100)
                self.x = range(len(self.y))
                self.data_line.setData(self.x, self.y)  # Update the data.
                self.yield_over_time.append(int(sum(self.passed_every_50) / self.calculate_on * 100))
            if 0 < len(self.y) != self.prev_y_len and self.yield_was_high_lately:
                self.prev_y_len = len(self.y)
                if self.y[-1] == 0:  # 50 fails in a row => Pause the run
                    msg = 'There are {} fails in a row, please make sure everything is OK,\nRun will stop if stop criteria is not ignored'.format(
                        str(self.calculate_on))
                    printing_func(msg, 'MainWindow', lock_print, logger_type='warning',
                                  logger_name=self.ports_and_guis.my_logger.logger.name)
                    self.yield_drop_happened = True
                    self.yield_was_high_lately = False
                    if not self.ignore_stop_conditions:
                        self.events.done_to_tag_thread.set()
                        self.events.done_to_r2r_thread.set()
                    else:
                        pass
                    self.events.stop_to_r2r_thread.set()
                elif self.y[-1] < int(self.minyield) and len(
                        self.y) > 15:  # under 40% yield-over-time for 200 tags => Pause the run
                    self.yield_drop_happened = True
                    for ii in range(1, 15):
                        if self.y[-ii] < int(self.minyield):
                            continue
                        else:
                            self.yield_drop_happened = False
                            break
                    if self.yield_drop_happened and not self.no_gui:
                        msg = str('*' * 100) + '\nThe yield-over-time of the last 200 tags is below {}%,' \
                                               ' Run will stop if stop criteria is not ignored\n'.format(
                            str(self.minyield)) + str('*' * 100)
                        printing_func(msg, 'MainWindow', lock_print, logger_type='warning',
                                      logger_name=self.ports_and_guis.my_logger.logger.name)
                        self.yield_was_high_lately = False
                        if not self.ignore_stop_conditions:
                            self.events.done_to_tag_thread.set()
                            self.events.done_to_r2r_thread.set()
                        else:
                            pass
                elif self.y[-1] > 50 and len(self.y) > 15:
                    self.yield_was_high_lately = True
            global yield_over_time
            yield_over_time = self.yield_over_time
            # update the prev counters
            self.last_tested_num += 1
            if passed > self.last_passed_num:
                self.last_passed_num += 1

        if tested == desired_tags_num and not self.first_reached_to_desired_tags:
            msg = '---------------------------Desired tags have reached (' + str(tested) + \
                  ') , If you wish to proceed, press Continue---------------------------'
            printing_func(msg, 'MainWindow', lock_print, logger_type='debug',
                          logger_name=self.ports_and_guis.my_logger.logger.name)
            self.first_reached_to_desired_tags = True
            self.stop_fn()
        if passed == desired_pass_num and not self.first_reached_to_desired_passes:
            msg = '---------------------------Desired passes have reached (' + str(passed) + \
                  ') , If you wish to proceed, press Continue---------------------------'
            printing_func(msg, 'MainWindow', lock_print, logger_type='debug',
                          logger_name=self.ports_and_guis.my_logger.logger.name)
            self.first_reached_to_desired_passes = True
            self.stop_fn()
        if not self.waiting_for_user_to_press_stop_because_printer:
            self.look_for_exceptions()

        if self.events.stop_main_trigger.isSet() and self.no_gui:
            self.events.stop_main_trigger.clear()
            self.tag_checker_thread.closure_fn()
            self.stop_fn()

    def look_for_exceptions(self):
        """
        search for exceptions in the threads Exceptions Queues.
        """
        if self.to_print:
            if not self.printer.exception_queue.empty() or not self.tag_checker_thread.exception_queue.empty() or \
                    not self.r2r_thread.exception_queue.empty():
                msg = "Paused because an exception happened, the R2R will pause now " \
                      "(the current spot will be fail)"
                printing_func(msg, 'MainWindow', lock_print, logger_type='debug',
                              logger_name=self.ports_and_guis.my_logger.logger.name)
                self.events.stop_to_r2r_thread.set()
                self.handle_r2r_exception()
        elif not self.tag_checker_thread.exception_queue.empty() or not self.r2r_thread.exception_queue.empty():
            msg = "Stopped because an exception happened, the R2R will pause now (the current spot will be fail)"
            printing_func(msg, 'MainWindow', lock_print, logger_type='debug',
                          logger_name=self.ports_and_guis.my_logger.logger.name)
            self.events.stop_to_r2r_thread.set()
            self.handle_r2r_exception()

    def handle_r2r_exception(self):
        """
        handle the exception if possible. prints the exception to screen and log
        """
        if self.to_print:
            if not self.printer.exception_queue.empty():
                exception_details = self.printer.exception_queue.get()
                msg = 'Printer got an Exception:'
                printing_func(msg, 'MainWindow', lock_print, logger_type='warning', do_log=True,
                              logger_name=self.ports_and_guis.my_logger.logger.name)
                # using logging.warning that will be parsed to errors
                print_exception(exception_details, printing_lock=lock_print)
                exc_type, exc_obj, exc_trace = exception_details
                # ConnectionResetError => exc_obj = 'An existing connection was forcibly closed by the remote host'
                if isinstance(exc_obj, PrinterNeedsResetException):
                    self.exception_message = 'Run will stop, Printer needs restart'
                    printing_func(self.exception_message, 'MainWindow', lock_print, logger_type='warning', do_log=True,
                                  logger_name=self.ports_and_guis.my_logger.logger.name)
                    self.events.printer_error.set()  # to avoid deadlock when printer thread crashed before
                    self.stop_fn()
                elif isinstance(exc_obj, ConnectionResetError):
                    self.events.done_to_printer_thread.set()
                    self.exception_message = 'Will close socket to Printer and restart it, please wait...'
                    printing_func(self.exception_message, 'MainWindow', lock_print, logger_type='warning',
                                  logger_name=self.ports_and_guis.my_logger.logger.name)
                    self.events.printer_event.wait()
                else:
                    if self.events.r2r_ready.isSet():
                        self.events.r2r_ready.clear()
                    self.exception_message = 'Please check everything is OK and restart the run'
                    printing_func(self.exception_message, 'MainWindow', lock_print, logger_type='warning',
                                  logger_name=self.ports_and_guis.my_logger.logger.name)
                    self.stop_fn()
        if not self.tag_checker_thread.exception_queue.empty():
            exception_details = self.tag_checker_thread.exception_queue.get()
            self.exception_message = 'tag_checker_thread got an Exception, please restart the run'
            exc_type, exc_obj, exc_trace = exception_details
            if 'R2R moved before timer ended' in str(exc_obj):
                self.exception_message = 'R2R moved before timer ended, please check in r2r controller\n' \
                                         'Menu -> Motors setup -> DELAY BETWEEN STEPS\n' \
                                         'is set to 999'
                printing_func(self.exception_message, 'MainWindow', lock_print, logger_type='warning',
                              logger_name=self.ports_and_guis.my_logger.logger.name)
                print_exception(exception_details, printing_lock=lock_print)
                pop_up_window(self.exception_message)
            else:
                printing_func(self.exception_message, 'MainWindow', lock_print, logger_type='warning',
                              logger_name=self.ports_and_guis.my_logger.logger.name)
                print_exception(exception_details, printing_lock=lock_print)
            self.stop_fn()

        if not self.r2r_thread.exception_queue.empty():
            exception_details = self.r2r_thread.exception_queue.get()
            self.exception_message = 'r2r_thread got an Exception, please restart the run'
            printing_func(self.exception_message, 'MainWindow', lock_print, logger_type='debug',
                          logger_name=self.ports_and_guis.my_logger.logger.name)
            print_exception(exception_details, printing_lock=lock_print)
            self.stop_fn()

    def check_logging_due_to_printing_offset(self):
        # check logging due to printing offset:
        if self.ports_and_guis.Tag_Value['printOffset'] != 0:
            if self.tag_checker_thread.missing_labels_in_a_row < self.ports_and_guis.Tag_Value['printOffset']:
                packet_dict = csv_to_dict(path=self.ports_and_guis.my_logger.packets_data_path)
                n_not_printed = self.ports_and_guis.Tag_Value[
                                    'printOffset'] - self.tag_checker_thread.missing_labels_in_a_row
                if len(packet_dict['tag_run_location']):
                    last_tested_location = packet_dict['tag_run_location'][-1]
                    location_to_delete = []
                    for i in range(n_not_printed):
                        try:
                            location_to_delete.append(str(int(last_tested_location) + i))
                        except Exception as e:
                            self.ports_and_guis.my_logger.logger.warning(
                                'invalid last_tested_location {} could not clean all external id that were not printed due '
                                'to printing offset ({})'.format(last_tested_location, e))
                    failed_due_to_no_print = []
                    for i in range(len(packet_dict['tag_run_location'])):
                        if packet_dict['tag_run_location'][i] in location_to_delete:
                            packet_dict['external_id'][i] = ''
                            packet_dict['status_offline'][i] = '0'
                            if packet_dict['fail_bin_str'][i] == str(FailureCodes.PASS.name):
                                packet_dict['fail_bin'][i] = str(FailureCodes.NOT_PRINTED.value)
                                packet_dict['fail_bin_str'][i] = str(FailureCodes.NOT_PRINTED.name)
                                failed_due_to_no_print.append(packet_dict['tag_run_location'][i])

                    packet_dict_list = []
                    for i in range(len(packet_dict['common_run_name'])):
                        packet_dict_list.append({k: v[i] for k, v in packet_dict.items()})
                    with open(self.ports_and_guis.my_logger.packets_data_path, 'w', newline='') as f:
                        csv_writer = csv.DictWriter(f, packet_dict.keys())
                        csv_writer.writeheader()
                        csv_writer.writerows(packet_dict_list)
                        f.close()

                    # update run data:
                    run_dict = csv_to_dict(path=self.ports_and_guis.my_logger.run_data_path)
                    run_dict['total_run_passed_offline'][0] = \
                        str(int(run_dict['total_run_passed_offline'][0]) - len(list(set(failed_due_to_no_print))))
                    run_dict['run_offline_yield'][0] = \
                        str((int(run_dict['total_run_passed_offline'][0]) / int(run_dict['total_run_tested'][0])) * 100)
                    run_dict_list = [{k: v[0] for k, v in run_dict.items()}]
                    with open(self.ports_and_guis.my_logger.run_data_path, 'w', newline='') as f:
                        csv_writer = csv.DictWriter(f, run_dict.keys())
                        csv_writer.writeheader()
                        csv_writer.writerows(run_dict_list)
                        f.close()

def set_attn_power_offline(attn_obj, attn_power, simulation=False):
    """
    configure Attenuator to a specific value
    gets:
        attn_obj:       Attenuator obj
        attn_power:     value to set attn

    return:
        status if Attenuator is set correctly

    """
    if simulation:
        status = True
    else:
        status = True
        print('Setting Attenuator to {attn_power}dB'.format(attn_power=attn_power))
        attn_obj.Setattn(attn_power)
    return status


# --------  main code:  ---------- #
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_name', action='store', dest='file_name',
                        help='file_name - Test Configuration File Name (Json Format, *.json)')
    args = vars(parser.parse_args())
    config_file_name = args['file_name']

    app = QApplication([])
    window = MainWindow(test_config_path=config_file_name)
    app.exec_()
    # window.close()
    # sys.exit(0)
