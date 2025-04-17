FROM fdamador/openplc

COPY program/Machine_Statistics.st /home/openplc/program/
COPY run.sh /home/openplc/run.sh
RUN chmod +x /home/openplc/run.sh

CMD ["/home/openplc/run.sh"]

