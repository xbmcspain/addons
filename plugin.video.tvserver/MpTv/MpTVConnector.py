import urllib
import socket
import re
import xbmcgui
import xbmc

class MpTVConnector:
   '''demonstration class only 
     - coded for clarity, not efficiency'''


   def __init__(self, sock=None):
      if sock is None:
         self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
      else:
         self.sock = sock


   def mysend(self, msg):
      totalsent = 0
      # print "Socket send: " + msg
      while totalsent < len(msg):
         sent = self.sock.send(msg[totalsent:])
         if sent == 0:
            raise RuntimeError, "socket connection broken"
         totalsent = totalsent + sent


   def myreceive(self):
      fs = self.sock.makefile()
      read = fs.readline().rstrip()
      
      matches = re.compile('^error;(.*)').findall(read)
      if matches == []:
         # print "Socket receive: " + msg
         return read;
      else:
         xbmcgui.Dialog().ok("Server error", "Details: " + matches[0] + ".\n")
      
      return read


   def connect(self, host, port):
      try:
         self.sock.connect((host, port))
      except:
         #! Stop the script from being executed!
         xbmcgui.Dialog().ok("Error", "Server is offline or unavailable.\n")
         return

      # connect and send the protocol
      self.mysend("TVServerXBMC:0-2\n")

      # make sure that what we receive is correct
      data = self.myreceive()

      if(re.compile("^Protocol-Accept;0-[2-9][^0-9]$").search(data)):
         raise RuntimeError, "not the right protocol : " + data
      else:
         print "[tvserver] Connection made"
   

   def getArguments( self, line ):
      list = line.split(";")
      for i in range(0, len(list)):
         list[i] = urllib.unquote(list[i])
      
      return list


   def getArgumentsList( self, line ):
      list = line.split(",")
      for i in range(0, len(list)):
         list[i] = self.getArguments(urllib.unquote(list[i]))
      
      return list


   # return a list of the group names, list<string>
   def getGroups( self ):
      self.mysend("ListGroups:\n")
      groupsLine = self.myreceive()

      groups = self.getArgumentsList(groupsLine)
      for i in range(0, len(groups)):
         groups[i] = groups[i][0]

      return groups

   
   # returns a list of pairs. pair = (id, name)
   def getChannels( self, group ):
      self.mysend("ListChannels:" + urllib.quote(group) + "\n")
      channelsLine = self.myreceive()
      channels = self.getArgumentsList(channelsLine)

      return channels


   def timeshiftChannel( self, chanId ):
      self.mysend("TimeshiftChannel:" + str(chanId) + "\n")
      result = self.myreceive()

      return result


   def stopTimeshift ( self ):
      self.mysend("StopTimeshift:\n")
      result = self.myreceive()


   def isTimeshifting ( self ):
      self.mysend("IsTimeshifting:\n")
      result = self.myreceive()
      timeshiftInfo = self.getArgumentsList(result)[0];
      return timeshiftInfo


   # return a list of the show names, list<string>
   def getShows( self ):
      self.mysend("ListRecordedTV:\n")
      showsLine = self.myreceive()
      xbmc.output ("Show: " + showsLine)
      shows = self.getArgumentsList(showsLine)

      return shows

   # delete a given show
   def deleteShow( self, recId ):
      self.mysend("DeleteRecordedTv:" + str(recId) + "\n")
      result = self.myreceive()

      return result


   def __del__(self):
      # destructor will kill the connection
      self.mysend("CloseConnection:\n")
      self.sock.close()
