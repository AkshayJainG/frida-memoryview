
var watchAddr = 0;
var forwardFlag = false;

rpc.exports = {
    readmem: function (address,size) {
        try
        {
            if(ptr(address).isNull()==false)
            {
                return Memory.readByteArray(ptr(address),size);
            }
            else
            {
                return false;
            }
        }
        catch(e)
        {
            return false;
        }
    },
    writemem: function (address,buffer) {
        try
        {
            if(ptr(address).isNull()==false)
            {
              return Memory.writeByteArray(ptr(address),buffer,buffer.length);
            }
            else
            {
                return false;
            }
        }
        catch(e)
        {
            return false;
        }
    },
    check: function(){
      if(watchAddr==0)
        return 0;
      else{
        var tmp = watchAddr;
        watchAddr = 0;
        return tmp;
      }
    },
    forward: function(){
      forwardFlag = true;
      return 1;
    }
  };

//This implementation is probably naive.
var mutex = 0;
function intercept(address){
  var flag = 0;
  while(mutex==1)
  {
    Thread.sleep(0.1);
  }
  mutex = 1;
  console.log("intercept");
  watchAddr = parseInt(address);
  while(true)
  {
    if(forwardFlag==true)
    {
      forwardFlag = false;
      break;
    }
    Thread.sleep(0.1);
  }
  mutex = 0;
} 


//This is example.
Interceptor.attach(Module.findExportByName(null,"fopen"), {
  onEnter: function (args) {
    console.log(args[0]);
    intercept(args[0]);
  },
  onLeave: function (retval) {
  }
});
