/* Python-EPICS channel access interface module  */
/* #ver1.1-1.5 written by Noboru Yamamoto, KEK, JAPAN */
/* modified to adopt EPICS.3.14.x , including threading */
/* add  

_ca _ca.c -DWITH_TK -DUNIX -I/proj/local/$(ARCH)/include \
-I$(EPICS_BASE)/include -L$(EPICS_BASE)/lib/hppa8k  \
-lca -lAs -lCom -lDb -lCompat

in Setup.local in Module directrory. You may omitt -lCompat on some platform. 
A macro WITH_TK should be defined when _ca.c used with Python/Tkinter.
A matching version of  python module "ca.py" is required togather wit this 
module.

For MacOSX with EPICS-R314:

EPICS_BASE=/Users/Shared/SRC/EPICS/R314/base-3.14.1
_ca _ca.c -DWITH_TK -DUNIX -I/usr/X11R6/include \
-I$(EPICS_BASE)/include -I$(EPICS_BASE)/include/os/Darwin -I$(EPICS_BASE)/include/os  -L$(EPICS_BASE)/lib/darwin-ppc -lca -lasHost -lCom 

*/

char * _Py_ca_version="$Revision: 1.1 $";


#if defined( Darwin ) || defined(HP_UX)
#  include <stdarg.h>
#elif defined( OSF1 ) 
#  include <varargs.h>
#else
#  include <varargs.h>
#endif
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <ctype.h>
#include <errno.h>

#include "Python.h"

#ifdef WITH_TK
#include <tk.h>
#endif

#define DEBUG 0
#undef DEBUG

#include <epicsVersion.h>
#include <errlog.h>
#include <caerr.h>
#include <cadef.h>

#define ca_message(STATUS) \
(ca_message_text[CA_EXTRACT_MSG_NO((STATUS))])

static void exceptionCallback(struct exception_handler_args args);
static int exceptionCallbackFormated(long, const char *, int, const char *, ...);


#define CA_PEND_EVENT_TIME	1e-6		/* formerly 0.0001    */
#define CA_MAX_RETRY 1000


#define TS2secs(ts) ((double)ts.secPastEpoch + (double) ts.nsec*1.0e-9)

/* function prototypes */
static void setup_alarm(void);
static void alarm_handler(int arg);
static void Py_ca_service(void);

static void Py_ca_fd_register(void *pfdctx,int	fd,int condition);
static PyObject *GetValfromArgs(struct event_handler_args args);
static PyObject *
_convert_ca_to_Python(chtype type, long count, void *pvalue, int satus);
static int
_convert_Py_to_ca(chtype type,long count, PyObject *val, void *pbuf);

static PyObject *Py_ca_search(PyObject *self, PyObject *args);
static PyObject *Py_ca_clear(PyObject *self, PyObject *args);
static PyObject *Py_ca_get(PyObject *self, PyObject *args);
static PyObject *Py_ca_put(PyObject *self, PyObject *args);
static PyObject *Py_ca_monitor(PyObject *self, PyObject *args);
static PyObject *Py_ca_clear_monitor(PyObject *self, PyObject *args);
static PyObject *Py_ca_pend_io(PyObject *self, PyObject *args);
static PyObject *Py_ca_test_io(PyObject *self, PyObject *args);
static PyObject *Py_ca_pend_event(PyObject *self, PyObject *args);
static PyObject *Py_ca_poll(PyObject *self, PyObject *args);
static PyObject *Py_ca_flush(PyObject *self, PyObject *args);
static PyObject *Py_ca_status(PyObject *self, PyObject *args);
static PyObject *Py_add_fd_registration(PyObject *self, PyObject *args);
static PyObject *Py_ca_channelInfo(PyObject *self, PyObject *args);
static PyObject *Py_ca_fileno(PyObject *self, PyObject *args);
static PyObject *Py_start_alarm(PyObject *self, PyObject *args);
static PyObject *Py_stop_alarm(PyObject *self, PyObject *args);

static PyObject *Py_sg_create(PyObject *self, PyObject *args);
static PyObject *Py_sg_delete(PyObject *self, PyObject *args);
static PyObject *Py_sg_block(PyObject *self, PyObject *args);
static PyObject *Py_sg_test(PyObject *self, PyObject *args);
static PyObject *Py_sg_reset(PyObject *self, PyObject *args);
static PyObject *Py_sg_put(PyObject *self, PyObject *args);
static PyObject *Py_sg_get(PyObject *self, PyObject *args);
static PyObject *Py_ca_convert(PyObject *self, PyObject *args);
static PyObject *Py_ca_task_exit(PyObject *self, PyObject *args);

/*  Method Table  */
static PyMethodDef CA_Methods[]={
  /* name in Python, function, flag(1 always), doc(str*) */
   {"search", Py_ca_search, 1,"EPICS CA search_and_connect"}, 
   {"clear", Py_ca_clear, 1,"EPICS CA channel close"},
   {"get", Py_ca_get, 1, "EPICS CA: get value in native form"},
   {"put", Py_ca_put,1, "EPICS CA:put value"},
   {"monitor", Py_ca_monitor,1,"EPICS CA:set up monitor callback"},
   {"clear_monitor", Py_ca_clear_monitor,1,"EPICS CA:delete monitor callback"},
   {"pendio", Py_ca_pend_io,1,"EPICS CA: wait for io completion"},
   {"pend_io", Py_ca_pend_io,1,"EPICS CA: wait for io completion"},
   {"test_io", Py_ca_test_io,1,"EPICS CA: test outstandig IO queries."},
   {"pend_event", Py_ca_pend_event,1,
    "EPICS CA: wait for next event(monitor, Archive, Alarm)"},
   {"poll", Py_ca_poll, 1, "EPICS CA: poll CA event(monitor, Archive, Alarm)"},
   {"flush", Py_ca_flush,1,"EPICS CA: flush CA buffer"},
   {"status", Py_ca_status, 1,"EPICA CA:connection status(0=connected)"},
   {"ch_info",Py_ca_channelInfo,1,"EPICS CA: channel info"},
   {"fileno",Py_ca_fileno,1,"EPICS CA: socket id "},
   {"add_fd_registration", Py_add_fd_registration,1,
    "Add file descriptor registration routine"},
   {"start_alarm",Py_start_alarm,1,""},
   {"stop_alarm",Py_stop_alarm,1,""},
   {"sg_create",Py_sg_create,1,"create sync. group id"},
   {"sg_delete",Py_sg_delete,1,"delete sync. group id"},
   {"sg_block",Py_sg_block,1,"wait for sync group operation"},
   {"sg_test",Py_sg_test,1,"test completion of sync group operation."},
   {"sg_reset",Py_sg_reset,1,"reset a sync group status"},
   {"sg_put",Py_sg_put,1,"issue a put request in a sync group"},
   {"sg_get",Py_sg_get,1,"issue a get request in a sync group"},
   {"ca_convert",Py_ca_convert,1,"Convert value returned by CA to PyObject"},
   {"__ca_task_exit",Py_ca_task_exit, 1, "Terminate CA libary"},
   {NULL, NULL, 0, NULL}
 };

/* error objects */
static PyObject *CaError;

/* glue routines to call Python code as callback */
static void  get_callback(struct event_handler_args );
#ifdef DEBUG
static void  get_callback_0(struct event_handler_args );
static void  get_callback_1(struct event_handler_args );
static void  get_callback_2(struct event_handler_args );
static void  get_callback_3(struct event_handler_args );
#else
#define get_callback_0 get_callback
#define get_callback_1 get_callback
#define get_callback_2 get_callback
#define get_callback_3 get_callback
#endif

static void  put_callback(struct event_handler_args);
static void  execCallBack(struct connection_handler_args);

typedef struct _ca_frame{
  PyObject *pfunc;
  PyThreadState *tstate;
  int purgeble;
} _ca_frame;


#undef WITH_THREAD  /* don't use thread for NOW. NY Dec.13,2000 */

#if defined( WITH_THREAD) && 0
#include <pthread.h>
#include "pythread.h"

/* Python/Tk/EPICS-CA needs thread lock to be thread ready */
/* routines in _ca.c may be called from ether Python interpreter or
   Tkinter context as a result of callback. */

static PyThread_type_lock ca_lock = 0;

  static struct ca_client_context *my_cac;
  static PyThreadState *ca_tstate = NULL;

#define ENTER_CA \
	{ PyThreadState *tstate = PyThreadState_Get(); Py_BEGIN_ALLOW_THREADS \
	    if(ca_lock)PyThread_acquire_lock(ca_lock, 1); ca_tstate = tstate;\
            if( ca_current_context() == NULL ){ca_attach_context(my_cac);}

#define LEAVE_CA \
    ca_tstate = NULL; if(ca_lock)PyThread_release_lock(ca_lock); Py_END_ALLOW_THREADS}

#define ENTER_OVERLAP \
	Py_END_ALLOW_THREADS

#define LEAVE_OVERLAP_CA \
	ca_tstate = NULL; if(ca_lock)PyThread_release_lock(ca_lock); }

#define ENTER_PYTHON \
	{ PyThreadState *tstate = ca_tstate; ca_tstate = NULL; \
	    if(ca_lock)PyThread_release_lock(ca_lock); if(tstate) PyEval_RestoreThread((tstate)); }

#define LEAVE_PYTHON \
	{ PyThreadState *tstate = PyEval_SaveThread(); \
	    if(ca_lock)PyThread_acquire_lock(ca_lock, 1); ca_tstate = tstate; }

#else

#define ENTER_CA
#define LEAVE_CA
#define ENTER_OVERLAP
#define LEAVE_OVERLAP_CA
#define ENTER_PYTHON
#define LEAVE_PYTHON

#endif


/* initialization routine */
/* module name and a initialization routine are registered in the inittab record in PyConfig.c */

/*# define CA_POLL_INTERVAL 160000 */
#define CA_POLL_INTERVAL 1000000 /*better to call ca_pend_event periodically*/

#define Check_Connection(_ch_id, _fname) {\
  int status=ECA_NORMAL;\
  if(!(_ch_id)){\
    PyErr_SetString(CaError, "Null channel ID as an argument");\
    return NULL;\
  }\
  \
  if( ca_state((_ch_id)) == cs_closed ) {\
      PyErr_SetString(CaError,"Invalid Channel");\
      return NULL;\
  }\
  else if( ca_state((_ch_id)) != cs_conn ) {\
      { \
         ENTER_CA \
         status=ca_pend_io(1.0); /* wait for ch_id to connect */\
         LEAVE_CA \
      }\
    SEVCHK(status,(_fname));\
    if (status != ECA_NORMAL){\
      PyErr_SetString(CaError,ca_message(status));\
      return NULL;\
    }\
  }\
\
  if( ca_state(_ch_id) != cs_conn ) { /* still not connected */\
    PyErr_SetString(CaError,"channel is not connected");\
    return NULL;\
  }\
}

static PyObject *saved_exitfunc=NULL;

static PyObject *Py_ca_task_exit(PyObject *self, PyObject *args)
{
  PyObject *res;


  ENTER_CA{
/* ca_task_exit();*/
  }LEAVE_CA
  if (saved_exitfunc && PyCallable_Check(saved_exitfunc)){
     Py_XINCREF(saved_exitfunc);
     res=PyObject_CallObject(saved_exitfunc,(PyObject *) NULL);
     if (res == NULL){
       PyErr_Print();
     }
     Py_XDECREF(saved_exitfunc);
  }
  Py_XINCREF(Py_None);
  return Py_None;
}

void init_ca(void){
  int status;
  PyObject *m, *d;
  PyObject *caexit,*exitfunc=PySys_GetObject("exitfunc");
  
  m=Py_InitModule("_ca",CA_Methods);
  d=PyModule_GetDict(m);
  CaError = PyErr_NewException("_ca.error", NULL, NULL);
  PyDict_SetItemString(d,"calibError", CaError);
  PyDict_SetItemString(d, "error", CaError);

  /* CA initialization */
  /* set up file descriptor mgr and initialize channel access */
  SEVCHK(ca_context_create(ca_disable_preemptive_callback), 
	     "init_ca: C.A. initialize failure.\n");
#ifdef WITH_THREAD
  my_cac=ca_current_context();
#endif

  /* status=atexit((void (*)(void)) ca_task_exit); */
  /*saved_exitfunc=exitfunc; */
  caexit=PyDict_GetItemString(d,"__ca_task_exit");
  PySys_SetObject("exitfunc",caexit);
  
/*
  status=Py_AtExit((void (*)(void)) ca_context_destroy);
  if (status != 0){
    fprintf(stderr,"registration of ca_task_exit failed");
    exit(-1);
  }
*/
  ENTER_CA  
     status=ca_add_exception_event(exceptionCallback,NULL);
      SEVCHK(status, "init_ca: failed to register exception handler\n");
  ENTER_OVERLAP
      status=ca_add_fd_registration(Py_ca_fd_register, NULL);
      SEVCHK(status, "init_ca: Fd registration failed.\n");
  LEAVE_OVERLAP_CA
}

static PyObject *
Py_ca_search(PyObject *self, PyObject *args)
{
  static char *name;
  chid ch_id;
  int status;
  _ca_frame *pframe;
  
  int nc;
  PyObject *pcallback;
  
  if(!PyArg_ParseTuple(args,"z#O",&name,&nc,&pcallback))
    return NULL;
  
  if (!name || !nc ) {
    PyErr_SetString(CaError, "Empty channel Name");
    return NULL; /* NULL trigers Exception */
  }
  
  Py_XINCREF(pcallback);
  
  if (! PyCallable_Check(pcallback) ){
    ENTER_CA
      status=ca_search_and_connect(name, &ch_id, NULL, NULL); 
    
    LEAVE_CA
    }
  else{
    pframe=(_ca_frame *) malloc(sizeof(_ca_frame));
    pframe->pfunc=pcallback;
    pframe->tstate=PyThreadState_Get();
    pframe->purgeble=0; /* this CB is called when connection status chanes. 
			   So, do not delete this callback */
    ENTER_CA
      status = ca_create_channel(name, execCallBack, pframe, 0 , &ch_id);
    LEAVE_CA
      
      }
  SEVCHK(status, "Py_ca_search:search and connect");

  if (status != ECA_NORMAL){
    PyErr_SetString(CaError, ca_message(status));
    return NULL;
  }
  else {
    ENTER_CA
      SEVCHK(ca_change_connection_event(ch_id, execCallBack),
	     "Py_ca_search:change_connection"); 
    LEAVE_CA
    return Py_BuildValue("l", ch_id);
  }
}

static PyObject *
Py_ca_clear(PyObject *self, PyObject *args){

  chid ch_id;
  int status;


  if(!PyArg_ParseTuple(args, "l", &ch_id))
    return NULL;

  if (!ch_id || ca_state(ch_id) == cs_never_conn ||ca_state(ch_id) == cs_closed ) {
    PyErr_SetString(CaError, "Null channel ID as an argument");
    return NULL; /* NULL trigers Exception */ 
  }

    {
       ENTER_CA
        status=ca_clear_channel(ch_id);
       LEAVE_CA
    }

  SEVCHK(status,"Py_ca_clear");
  if(status != ECA_NORMAL){
    PyErr_SetString(CaError,ca_message(status));
    return NULL;
  }
  return Py_BuildValue("i",status);
} 

static PyObject *
Py_ca_get(PyObject *self, PyObject *args){
  chid ch_id;
  int status=ECA_NORMAL;
  unsigned long ecount;
  chtype type;
  PyObject *pcallback;
  _ca_frame *pframe;
  
  if(!PyArg_ParseTuple(args,"lOll",&ch_id,&pcallback,&type,&ecount))
    return NULL;

  Check_Connection(ch_id,"Py_ca_get"); /* MACRO for channel connection checking */

#ifdef DEBUG
#  if DEBUG
  fprintf(stderr,"set up callback for get. requested data type is %d\n",
	  ca_field_type(ch_id));  
#  endif
#endif

  if (type == -1){
    type = dbf_type_to_DBR_TIME(ca_field_type(ch_id));
  }
#if (( EPICS_VERSION == 3 ) && ( EPICS_REVISION == 14 ))
          /* keep ecount == 0 */
#else
  if (ecount==0){
    ecount=ca_element_count(ch_id);
  }
#endif
    Py_XINCREF(pcallback);
    pframe=(_ca_frame *) malloc(sizeof(_ca_frame));
    pframe->pfunc=pcallback;
    pframe->tstate=PyThreadState_Get();
    pframe->purgeble=1;
    {ENTER_CA
	status=ca_array_get_callback(type, ecount,
				   ch_id, get_callback_0, pframe);
     LEAVE_CA}
  if(status != ECA_NORMAL){
    PyErr_SetString(CaError,ca_message(status));
    Py_XDECREF(pcallback);
    return NULL;
  }
  return Py_BuildValue("i",status);
}


typedef dbr_string_t *dbr_string_t_ptr;
typedef dbr_char_t *dbr_char_t_ptr ;

#define MoveDBRtoValue(DBRTYPE, VP, PYTYPE, FORMAT) \
     {\
       struct dbr_sts_##DBRTYPE  *cval=(struct dbr_sts_##DBRTYPE  *)val;\
       register dbr_##DBRTYPE##_t *vp=(dbr_##DBRTYPE##_t *)(VP);\
       register int cur;\
       arglist=Py_BuildValue("((Oii))",array,\
			     (int) cval->severity,(int) status);\
       Py_XDECREF(array);\
       for (cur=0;cur < count; cur++){\
	 PyObject *ent=Py_BuildValue(FORMAT,(PYTYPE) *vp++);\
	 PySequence_SetSlice(array,cur,cur,ent);\
	 Py_XDECREF(ent);\
       }\
     }

#define MoveTimeDBRtoValue(DBRTYPE, VP, PYTYPE, FORMAT) \
     {\
       struct dbr_time_##DBRTYPE  *cval=(struct dbr_time_##DBRTYPE  *)val;\
       register dbr_##DBRTYPE##_t *vp=(dbr_##DBRTYPE##_t *)(VP);\
       register int cur;\
       arglist=Py_BuildValue("((Oiid))",array, \
			     (int) cval->severity,(int) status,\
			     TS2secs(cval->stamp));\
       Py_XDECREF(array);\
       for (cur=0;cur < count; cur++){\
	 PyObject *ent=Py_BuildValue((FORMAT),(PYTYPE) *vp++);\
	 PySequence_SetSlice(array,cur,cur,ent);\
	 Py_XDECREF(ent);\
       }\
     }

/* dbx_xxx_yyy structures are defined in db_access.h in EPICS/base/include */

static void put_callback(struct event_handler_args args){

/*  PyObject *pcallback=NULL,*arglist=NULL,*result=NULL;*/

}

#ifdef DEBUG
static void get_callback_0(struct event_handler_args args){
  fprintf(stderr, "get_callback 0: \n");fflush(stderr);
  get_callback(args);
  fprintf(stderr, "done get_callback 0: \n");fflush(stderr);
}

static void get_callback_1(struct event_handler_args args){
  fprintf(stderr, ">get_callback 1: \n");fflush(stderr);
  get_callback(args);
  fprintf(stderr, "<done get_callback 1: \n");fflush(stderr);
}

static void get_callback_2(struct event_handler_args args){
  fprintf(stderr, ">>get_callback 2: \n");fflush(stderr);
  get_callback(args);
  fprintf(stderr, "<<done get_callback 2: \n");fflush(stderr);
}

static void get_callback_3(struct event_handler_args args){
  fprintf(stderr, ">>>get_callback 3: \n");fflush(stderr);
  get_callback(args);
  fprintf(stderr, "<<<done get_callback 3: \n");fflush(stderr);
}
#endif

static void get_callback(struct event_handler_args args)
{
  int status;
  PyObject *pcallback=NULL,*arglist=NULL,*result=NULL;
  _ca_frame *pframe;
  PyThreadState *tstate;

  ENTER_PYTHON
    
  pframe=(_ca_frame *)args.usr;
  status=args.status;
  
  if (pframe){

    pcallback=pframe->pfunc;
    tstate=pframe->tstate;

    /*restore thread state to that of callback is defined */
    if(tstate) PyEval_RestoreThread(tstate);
    {
      arglist=GetValfromArgs(args);
      if (arglist == (PyObject *) NULL){
	arglist=PyTuple_New(0);
	Py_XINCREF(arglist);
      }
    
      /* call callback routine with arglist -> do whatever it likes */
      Py_XINCREF(pcallback);
      if (PyCallable_Check(pcallback)){
#ifdef DEBUG
	fprintf(stderr,"]] calling Python callback\n");fflush(stderr);
#endif
	result=PyObject_CallObject(pcallback,arglist);
#ifdef DEBUG
	fprintf(stderr,"[[ done Python callback\n");fflush(stderr);
#endif
      }
#ifdef DEBUG
      else{
	fprintf(stderr,"CallBack is not callable\n");fflush(stderr);
      }
#endif
      Py_XDECREF(arglist); Py_XDECREF(result); Py_XDECREF(pcallback); 
      if (pframe->purgeble) {
	free(pframe);
	Py_XDECREF(pcallback);
      }
    }
  }
  else{
    fprintf(stderr, "No execution environment(pframe)\n");
  }
  LEAVE_PYTHON
}

static PyObject *GetValfromArgs(struct event_handler_args args){
  PyObject *retObj; 
  retObj=_convert_ca_to_Python(args.type, args.count, 
			       (void *) args.dbr, args.status);
  return retObj;
}

static PyObject *
_convert_ca_to_Python(chtype type, long count, void *val, int status){

  PyObject *arglist=NULL;
  PyObject *array=NULL;

  if(!val){
     return (PyObject *) NULL;
  }
  else{
    if(count==1){
      switch(type){
      case DBR_STRING:
	arglist=Py_BuildValue("((si))",((char *) val),status);
	break;
      case DBR_INT:
      case DBR_ENUM:
	arglist=Py_BuildValue("((ii))",*((short *) val),status);
	break;
      case DBR_FLOAT:
	arglist=Py_BuildValue("((fii))",*((float *) val),-1,status);
	break;
      case DBR_CHAR:
	arglist=Py_BuildValue("((bii))",((char *) val),-1,status);
	break;
      case DBR_LONG:
	arglist=Py_BuildValue("((lii))",*((long *) val),-1,status);
	break;
      case DBR_DOUBLE:
	arglist=Py_BuildValue("((dii))",*((double *) val),-1,status);
	break;
      case DBR_TIME_STRING:
	{
	  struct dbr_time_string *cval=val;
	  arglist=Py_BuildValue("((siid))",
				cval->value, cval->severity, cval->status,
				TS2secs(cval->stamp));
	}
	break;
	/*   case DBR_TIME_INT: */
      case DBR_TIME_SHORT:	
	{
	  struct dbr_time_short  *cval=val;
	  arglist=Py_BuildValue("((iiid))",
				cval->value, cval->severity, cval->status,
				TS2secs(cval->stamp));
	}
	break;
      case DBR_TIME_ENUM:
	{
	  struct dbr_time_enum  *cval=val;
	  arglist=Py_BuildValue("((iiid))",cval->value,cval->severity,
				cval->status,
				TS2secs(cval->stamp));
	}
	break;
      case DBR_TIME_FLOAT:
	{
	  struct dbr_time_float  *cval=val;
	  arglist=Py_BuildValue("((fiid))",
				cval->value, cval->severity, cval->status,
				TS2secs(cval->stamp));
	}
	break;
      case DBR_TIME_CHAR:
	{
	  struct dbr_time_char *cval=val;
	  arglist=Py_BuildValue("((biid))", 
				cval->value, cval->severity, cval->status,
				TS2secs(cval->stamp));
	}
	break;
      case DBR_TIME_LONG:
	{
	  struct dbr_time_long  *cval=val;
	  arglist=Py_BuildValue("((liid))",
				cval->value,cval->severity,cval->status,
				TS2secs(cval->stamp));
	}
	break;
      case DBR_TIME_DOUBLE:
	{
	  struct dbr_time_double  *cval=val;
	  arglist=Py_BuildValue("((diid))",
				cval->value, cval->severity, cval->status,
				TS2secs(cval->stamp));
	}
	break;
      case DBR_CTRL_CHAR:
	{
	  struct dbr_ctrl_char *cval=(struct dbr_ctrl_char *) val;
	  arglist=Py_BuildValue("((biid(sdddddddd)))",
				cval->value,
				cval->severity,
				cval->status,
				0.0,
				cval->units,
				cval->upper_disp_limit,
				cval->lower_disp_limit,
				cval->upper_alarm_limit,
				cval->upper_warning_limit,
				cval->lower_alarm_limit,
				cval->lower_warning_limit,
				cval->upper_ctrl_limit,
				cval->lower_ctrl_limit
				);
	}
	break;
      case DBR_CTRL_LONG:
	{
	  struct dbr_ctrl_long *cval=(struct dbr_ctrl_long *) val;
	  arglist=Py_BuildValue("((liid(sdddddddd)))",
				cval->value,
				cval->severity,
				cval->status,
				0.0,
				cval->units,
				cval->upper_disp_limit,
				cval->lower_disp_limit,
				cval->upper_alarm_limit,
				cval->upper_warning_limit,
				cval->lower_alarm_limit,
				cval->lower_warning_limit,
				cval->upper_ctrl_limit,
				cval->lower_ctrl_limit
				);
	}
	break;
      case DBR_CTRL_DOUBLE:
	{
	  struct dbr_ctrl_double *cval=(struct dbr_ctrl_double *) val;
	  arglist=Py_BuildValue("((diid(sddddddddi)))",
				cval->value,
				cval->severity,
				cval->status,
				0.0,
				cval->units,
				cval->upper_disp_limit,
				cval->lower_disp_limit,
				cval->upper_alarm_limit,
				cval->upper_warning_limit,
				cval->lower_alarm_limit,
				cval->lower_warning_limit,
				cval->upper_ctrl_limit,
				cval->lower_ctrl_limit,
				cval->precision
				);
	}
	break;
      case DBR_CTRL_ENUM:
	{
	  struct dbr_ctrl_enum *cval=(struct dbr_ctrl_enum *) val;
	  char (*strs)[][MAX_ENUM_STRING_SIZE]=&cval->strs;
	  int nstr=cval->no_str,i;
	  PyObject *ptup=PyTuple_New(nstr);

	  for(i=0; i< nstr;i++){
	    PyTuple_SET_ITEM(ptup,i,PyString_FromString((*strs)[i]));
	  }
	  arglist=Py_BuildValue("((iiid(iO)))",
				cval->value,
				cval->severity,
				cval->status,
				0.0,
				cval->no_str,
				ptup
				);
	  Py_XDECREF(ptup);
	}
	break;
      default:
	arglist=Py_BuildValue("((lii))",*((long *) val),-1,status);
      }
    }
    else{/* wave form/array data */
      array=PyList_New(0); /* create Empty python-list object */
      if(array == NULL){
	PyErr_SetString(CaError,"Cannot create list");
	Py_XDECREF(arglist);
	return (PyObject *) NULL;
      }
      switch(type){
      case DBR_STRING:
	MoveDBRtoValue(string, cval->value, dbr_string_t_ptr, "[z]");
	break;
      case DBR_CHAR:
	MoveDBRtoValue(char, &(cval->value), dbr_char_t, "[b]");
	break;
      case DBR_FLOAT:
	MoveDBRtoValue(float, &(cval->value), float , "[f]");
	break;
      case DBR_SHORT:/* same as DBR_TIME_INT */
	MoveDBRtoValue(short, &(cval->value), int, "[i]");
	break;
      case DBR_ENUM:
	MoveDBRtoValue(enum, &(cval->value), int, "[i]");
	break;
      case DBR_LONG:
	MoveDBRtoValue(long, &(cval->value), long, "[l]");
	break;
      case DBR_DOUBLE:
	MoveDBRtoValue(double, &(cval->value), double, "[d]");
	break;
      case DBR_TIME_STRING:
	MoveTimeDBRtoValue(string, cval->value, dbr_string_t_ptr, "[z]");
	break;
      case DBR_TIME_CHAR:
	MoveTimeDBRtoValue(char, &(cval->value), dbr_char_t, "[b]");
	break;
      case DBR_TIME_FLOAT:
	MoveTimeDBRtoValue(float, &(cval->value), float , "[f]");
	break;
      case DBR_TIME_SHORT:/* same as DBR_TIME_INT */
	MoveTimeDBRtoValue(short, &(cval->value), int, "[i]");
	break;
      case DBR_TIME_ENUM:
	MoveTimeDBRtoValue(enum, &(cval->value), int, "[i]");
	break;
      case DBR_TIME_LONG:
	MoveTimeDBRtoValue(long, &(cval->value), long, "[l]");
	break;
      case DBR_TIME_DOUBLE:
	MoveTimeDBRtoValue(double, &(cval->value), double, "[d]");
	break;
      default:
	PyErr_SetString(CaError,"Unkown Data Type");
	Py_XDECREF(array);
	Py_XDECREF(arglist);
	return (PyObject *) NULL;
      }
    }
  }
  return arglist;
}


static void execCallBack(struct connection_handler_args args)
{
  chid ch_id;
  PyObject *pcallback, *result, *arg;  
  struct _ca_frame *pframe;
  PyThreadState *tstate;

  ch_id=args.chid;
  pframe=(struct _ca_frame *) ca_puser(ch_id);
  ENTER_PYTHON
  if(pframe != NULL && 
     ((pcallback=pframe->pfunc) != Py_None)){ 
    
    tstate=pframe->tstate;
    if (tstate) PyEval_RestoreThread(tstate);
    Py_XINCREF(pcallback);
    /* call callback routine with arglist -> do whatever it likes */
    arg=Py_BuildValue("()");
    result=PyObject_CallObject(pcallback,arg);
    Py_XDECREF(arg);
    Py_XDECREF(pcallback); Py_XDECREF(result);
    if(pframe->purgeble){
      Py_XDECREF(pcallback);
      free(pframe);
    }
  }
  LEAVE_PYTHON
}

#define MoveValuesToBuffer(DBRBUFTYPE, DBRTYPE, FORMAT) \
      pbuf=calloc(count,sizeof(DBRTYPE));\
      if ( pbuf == NULL ){\
	PyErr_NoMemory();\
	return NULL;\
      }\
      {\
	DBRTYPE *ptr=(DBRTYPE *) pbuf;\
	DBRBUFTYPE buf;\
	for(cur=0;cur<count;cur++){\
	  item=PySequence_GetItem(value,cur);\
	  PyArg_Parse(item,FORMAT, &buf);\
	  ptr[cur]=(DBRTYPE) buf;\
	}\
   }	   

static PyObject *Py_ca_put(PyObject *self, PyObject *args)
{
  chid ch_id;
  int status=0;
  PyObject *value,*myval=NULL,*item=NULL,*pcallback;
  int count,retry=0;
  register int cur=0;
  char errmsg[80];
  static union  {
    double d;
    float f;
    char *str;
    int i;
    short int si;
    long l;
    PyObject * O;
  } v;
  void *pbuf;
  _ca_frame *pframe;

  /* now value is always Tuple. Sept. 26,97 */
  if(!PyArg_ParseTuple(args,"lOOO", &ch_id, &value, &myval, &pcallback))
    return NULL;

  Check_Connection(ch_id,"Py_ca_put"); /* MACRO for channel connection checking */
  if(!ch_id){

    PyErr_SetString(CaError, "Null channel ID as an argument");
    return NULL;
  }

  if( PySequence_Check(value) != 1){
    Py_XDECREF(value);
    Py_XDECREF(myval);
    Py_XDECREF(pcallback);
    return NULL;
  }
  Py_XINCREF(pcallback);

  count=PyObject_Length(value);
  while( ca_state(ch_id) == cs_never_conn ) {
      {  
	retry++;
	{ENTER_CA
	    ca_pend_io(0.1); /* wait for ch_id to connect */
	LEAVE_CA}
      }
      if (retry > CA_MAX_RETRY){
	PyErr_SetString(CaError, "Exceed Max retry to connect.");
	return NULL;
      }
  }
  
  if (count == 1){
    pbuf=malloc(sizeof(v)); /* too much memory for some record types */
    if ( pbuf == NULL ){
      PyErr_NoMemory();
      return NULL;
    }
    item=PySequence_GetItem(value,cur);
    switch(ca_field_type(ch_id)){
    case DBR_STRING:
      free(pbuf);
      PyArg_Parse(item,"z",&pbuf);
      break;
    case DBR_INT: /* DBR_SHORT == DBR_INT */ 
      PyArg_Parse(item,"i",(int *)pbuf); 
      *((short *) pbuf)=*((int *) pbuf); 
      break;
    case DBR_FLOAT:
      PyArg_Parse(item,"f",(float *) pbuf);
      break;
    case DBR_ENUM:
      PyArg_Parse(item,"i",(int *)pbuf);
      *((short *) pbuf)=*((int *) pbuf);
      break;
    case DBR_CHAR:
      PyArg_Parse(item,"b",pbuf);
      break;
    case DBR_LONG:
      PyArg_Parse(item,"l",(long *) pbuf);
      break;
    case DBR_DOUBLE:
      PyArg_Parse(item,"d",(double *) pbuf);
      break;
    default:
      sprintf(errmsg,"InvalidDataType %u", ca_field_type(ch_id));
      PyErr_SetString(CaError,errmsg);
      break;
    } 
      if (pcallback == Py_None ){
	ENTER_CA
	  status=ca_array_put(ca_field_type(ch_id),
			    count, ch_id, pbuf);
	LEAVE_CA
      }
      else{
	pframe=(_ca_frame *) malloc(sizeof(_ca_frame));
	pframe->pfunc=pcallback;
	pframe->tstate=PyThreadState_Get();
	pframe->purgeble=1;
        
        ENTER_CA
	  status=ca_array_put_callback(ca_field_type(ch_id),
				       count, ch_id, pbuf, 
				       get_callback_1, pframe);
        LEAVE_CA
      }
    if(ca_field_type(ch_id) !=DBR_STRING) free(pbuf);
    if(status != ECA_NORMAL) {
      PyErr_SetString(CaError, ca_message(status));
      if(item != NULL){  Py_DECREF(item);}
      return NULL;
    }
    return Py_BuildValue("i",status);
  } 
  else if (count > 1) {/* array records */
    switch(ca_field_type(ch_id)){
    case DBR_STRING:
      pbuf=calloc(count,sizeof(dbr_string_t));
      if ( pbuf == NULL ){
	PyErr_NoMemory();
	return NULL;
      }
      {
	register dbr_string_t *ptr=(dbr_string_t *) pbuf;
	char *str;
	for(cur=0;cur<count;cur++){
	  item=PySequence_GetItem(value,cur);
	  PyArg_Parse(item,"z",&str);
	  strncpy((char *)&(ptr[cur]),
		  str,sizeof(dbr_string_t));
	}
      }
      break;
    case DBR_INT:/* note that MoveValuesToBuffer is Macro */
      MoveValuesToBuffer(dbr_long_t, dbr_int_t, "i"); 
      break;
    case DBR_FLOAT:
      MoveValuesToBuffer(dbr_double_t, dbr_float_t, "d");
      break;
    case DBR_ENUM:
      MoveValuesToBuffer(dbr_long_t, dbr_enum_t, "l");
      break;
    case DBR_CHAR:
      MoveValuesToBuffer(dbr_char_t,dbr_char_t,"b");
      break;
    case DBR_LONG:
      MoveValuesToBuffer(dbr_long_t,dbr_long_t,"l");
      break;
    case DBR_DOUBLE:
      MoveValuesToBuffer(dbr_double_t,dbr_double_t,"d");
      break;
    default:
      PyErr_SetString(CaError,"Invalid field type");
      if(item != NULL) { Py_DECREF(item);}
      return NULL;
    }
    Py_DECREF(item);
    item=NULL;
      if (pcallback == Py_None ){
        ENTER_CA
	  status=ca_array_put(ca_field_type(ch_id),
			      count, ch_id, pbuf);
        LEAVE_CA
      }
      else{
	pframe=(_ca_frame *) malloc(sizeof(_ca_frame));
	pframe->pfunc=pcallback;
	pframe->tstate=PyThreadState_Get();
	pframe->purgeble=1;
        ENTER_CA
	  status=ca_array_put_callback(ca_field_type(ch_id),
				     count, ch_id, pbuf, 
				     get_callback_2, pframe);
        LEAVE_CA
      }
    if(!pbuf) {free(pbuf);}
    if(item != NULL)  { Py_XDECREF(item);}
    if(value != NULL) { Py_XDECREF(value); }
    if (status != ECA_NORMAL){
      PyErr_SetString(CaError,ca_message(status));
      return NULL;
    }
    return Py_BuildValue("i",status);
  }
  else{
    sprintf(errmsg,"InvalidDataType %u", ca_field_type(ch_id));
    PyErr_SetString(CaError,errmsg);
    return NULL;
  }
}


static PyObject *
Py_ca_monitor(PyObject *self, PyObject *args){
  chid ch_id;
  int status=0;
  unsigned long ecount=-1;
  chtype type;
  PyObject *pcallback;
  evid EVID;
  _ca_frame *pframe;

  if(!PyArg_ParseTuple(args,"lOl",&ch_id,&pcallback,&ecount))
    return NULL;

  Check_Connection(ch_id,"Py_ca_monitor"); /* MACRO for channel connection checking */

  type =dbf_type_to_DBR_TIME(ca_field_type(ch_id));
  Py_XINCREF(pcallback);
  pframe=(_ca_frame *) malloc(sizeof(_ca_frame));
  pframe->pfunc=pcallback;
  pframe->tstate=PyThreadState_Get();
  pframe->purgeble=0;
  if (ecount == 0){
    ecount=ca_element_count(ch_id);
  }

  {ENTER_CA
	status=ca_add_masked_array_event(type, ecount,
					 ch_id, get_callback_3, pframe, 
					 0.0, 0.0, 0.0,
					 &EVID, DBE_VALUE|DBE_ALARM
					 );
  LEAVE_CA}
  SEVCHK(status,"Py_monitor");
  return Py_BuildValue("l",EVID);
}

static PyObject *
Py_ca_clear_monitor(PyObject *self, PyObject *args){
  int status;
  evid EVID;

  if(!PyArg_ParseTuple(args,"l",&EVID))
    return NULL;
    if(!EVID){
      PyErr_SetString(CaError, "Null EVENT ID as an argument");
      return NULL;
    }
  {ENTER_CA
      status=ca_clear_event(EVID);
  LEAVE_CA}
  SEVCHK(status,"Py_Clear_monitor");
  /* we shoud call Py_XDECREF(pcallback) here. But how? */
  return Py_BuildValue("i",status);
} 

static PyObject *
Py_ca_pend_io(PyObject *self, PyObject *args){

  ca_real wait;
  int status ;

#if 0
  fprintf(stderr, ">> pend_io\n");
  fflush(stderr);
#endif

  if(!PyArg_ParseTuple(args,"d",&wait))
    return NULL;

  {ENTER_CA
      status=ca_pend_io(wait);
   LEAVE_CA}
#if 0
  fprintf(stderr, "<<done pend_io tmo:%f,status:%d\n",wait,status);
  fflush(stderr);
#endif
  SEVCHK(status,"py_pend_io");
  return Py_BuildValue("i",CA_EXTRACT_MSG_NO(status));
} 

static PyObject *
Py_ca_test_io(PyObject *self, PyObject *args){

  int status ;

    {ENTER_CA
	status=ca_test_io();
    LEAVE_CA}

  SEVCHK(status,"py_test_io");
  return Py_BuildValue("i",CA_EXTRACT_MSG_NO(status));
} 

static PyObject *
Py_ca_pend_event(PyObject *self, PyObject *args){
  ca_real wait;
  int status ;

  if(!PyArg_ParseTuple(args,"d",&wait))
    return NULL;

  {ENTER_CA
    status=ca_pend_event(wait);
  LEAVE_CA}
  return Py_BuildValue("i",CA_EXTRACT_MSG_NO(status));
}

static PyObject *
Py_ca_poll(PyObject *self, PyObject *args){

  int status ;
   
  {ENTER_CA
     status=ca_poll();
  LEAVE_CA}
 
  return Py_BuildValue("i",CA_EXTRACT_MSG_NO(status));
}

static PyObject *
Py_ca_flush(PyObject *self, PyObject *args){
  int status;

  {ENTER_CA
     status=ca_flush_io();
  LEAVE_CA}
  return Py_BuildValue("i",CA_EXTRACT_MSG_NO(status));
} 

static PyObject *
Py_ca_status(PyObject *self, PyObject *args){
  chid ch_id;
  int status ;

  if(!PyArg_ParseTuple(args,"l",&ch_id))
    return NULL;
  if(!ch_id){
    PyErr_SetString(CaError, "Null channel ID as an argument");
    return NULL;
  }

  status=ca_state(ch_id) - cs_conn;

  return Py_BuildValue("i",status);
} 

static PyObject *Py_ca_channelInfo(PyObject *self, PyObject *args){
  chid ch_id;

  if(!PyArg_ParseTuple(args,"l",&ch_id))
    return NULL;
  if(!ch_id){
    PyErr_SetString(CaError, "Null channel ID as an argument");
    return NULL;
  }
  return Py_BuildValue(
		    "(iilisii)",
		    ca_field_type(ch_id),
		    ca_element_count(ch_id),
		    ca_puser(ch_id),
		    ca_state(ch_id),
		    ca_host_name(ch_id),
		    ca_read_access(ch_id),
		    ca_write_access(ch_id)
		    );
} 

#define ca_sock_id(CHID)  ca_sock_id_function(CHID)

#if (EPICS_VERSION >=3) && (EPICS_REVISION >=14)

static int ca_sock_id_function(chid CHID){
  fprintf(stderr, "you cannot get sock id diretly. Use fd_register function , instead");
  return -1;
}
#endif

static PyObject *Py_ca_fileno(PyObject *self, PyObject *args){
  chid ch_id;
  int sock;

  if(!PyArg_ParseTuple(args,"l",&ch_id))
    return NULL;
  if(!ch_id){
    PyErr_SetString(CaError, "Null channel ID as an argument");
    return NULL;
  }
  sock=ca_sock_id(ch_id);
  return Py_BuildValue(
		    "i",
		    sock);
} 

static PyThreadState *fd_register_save_tstate;

static void Py_fd_register_wrapper(void *args, int fd, int condition)
{
  PyObject *func,*arg;
  PyObject *result, *uargs;

  ENTER_PYTHON
  if (fd_register_save_tstate) PyEval_RestoreThread(fd_register_save_tstate);
  func=PyTuple_GetItem((PyObject *) args,0);
  arg= PyTuple_GetItem(args,1);
  if (PyCallable_Check(func)){
    Py_XINCREF(func);
    uargs=Py_BuildValue("(Oii)",arg,fd, condition);
    Py_XINCREF(uargs);
    result=PyObject_CallObject(func, uargs);
    Py_XDECREF(func);Py_XDECREF(uargs);
  }
  fd_register_save_tstate=PyEval_SaveThread(); 
  LEAVE_PYTHON
}

static PyObject *Py_add_fd_registration(PyObject *self, PyObject *args){
  int status;
  PyObject *func, *arg;

  if(!PyArg_ParseTuple(args,"OO",&func, &arg))
    return NULL;

  if(!args){
    PyErr_SetString(CaError, "Null channel ID as an argument");
    return NULL;
  }
  Py_XINCREF(args);
  /* fd_register_save_tstate=PyEval_SaveThread();*/
  ENTER_CA
    status=ca_add_fd_registration(Py_fd_register_wrapper, args);
    SEVCHK(status,"add_fd_regstration: Fd registration failed.\n");
  LEAVE_CA
  Py_INCREF(Py_None);
  return Py_None;
} 


/************************ sync. group routines ****************************/
static PyObject *
Py_sg_create(PyObject *self, PyObject *args){

  int status;
  CA_SYNC_GID gid;

  {ENTER_CA

      status=ca_sg_create(&gid);
      SEVCHK(status, "Py_sg_create");
  LEAVE_CA}

  if (status != ECA_NORMAL){
    PyErr_SetString(CaError, ca_message(status));
    return NULL;
  }
  else {
    return Py_BuildValue("i", gid);
  }
}

static PyObject *
Py_sg_delete(PyObject *self, PyObject *args){

  int status;
  CA_SYNC_GID gid;

  if(!PyArg_ParseTuple(args,"i",&gid)){
    return NULL;
  }
  if(gid < 0){
    PyErr_SetString(CaError, "Null sync. Group ID as an argument");
    return NULL;
  }

  {ENTER_CA
      status=ca_sg_delete(gid);
  LEAVE_CA}

  SEVCHK(status, "Py_sg_delete")

  if (status != ECA_NORMAL){
    PyErr_SetString(CaError, ca_message(status));
    return NULL;
  }
  else {
    return Py_BuildValue("i", gid);
  }
}

static PyObject *
Py_sg_block(PyObject *self, PyObject *args){

  int status;
  CA_SYNC_GID gid;
  float tmo;

  if(!PyArg_ParseTuple(args,"if",&gid,&tmo)){
    return NULL;
  }
  if(gid < 0){
    PyErr_SetString(CaError, "Null sync. Group ID as an argument");
    return NULL;
  }
  {ENTER_CA
    status=ca_sg_block(gid,(tmo > 0.0 ? tmo:1.0));
  LEAVE_CA}

  switch(status){
  case ECA_NORMAL:
    return Py_BuildValue("i", 0);
    break;
  case ECA_TIMEOUT:
  case ECA_EVDISALLOW:
  case ECA_BADSYNCGRP:
  default:
    PyErr_SetString(CaError, ca_message(status));
    return NULL;
  }
}

static PyObject *
Py_sg_test(PyObject *self, PyObject *args){

  int status;
  CA_SYNC_GID gid;

  if(!PyArg_ParseTuple(args,"i",&gid)){
    return NULL;
  }
  if(gid < 0){
    PyErr_SetString(CaError, "Null sync. Group ID as an argument");
    return NULL;
  }

  {ENTER_CA
    status=ca_sg_test(gid);
    SEVCHK(status, "Py_sg_create");
  LEAVE_CA}

  switch(status){
  case ECA_IODONE:
    return Py_BuildValue("i", 0);
    break;
  case ECA_IOINPROGRESS:
    return Py_BuildValue("i", -1);
    break;
  default:
    PyErr_SetString(CaError, ca_message(status));
    return NULL;
  }
}

static PyObject *
Py_sg_reset(PyObject *self, PyObject *args){

  int status;
  CA_SYNC_GID gid;

  if(!PyArg_ParseTuple(args,"i",&gid)){
    return NULL;
  }

  if(gid < 0){
    PyErr_SetString(CaError, "Null Sync. Group ID as an argument");
    return NULL;
  }

  {ENTER_CA
    status=ca_sg_reset(gid);
    SEVCHK(status, "Py_sg_create")
  LEAVE_CA }

  if (status != ECA_NORMAL){
    PyErr_SetString(CaError, ca_message(status));
    return NULL;
  }
  else {
    return Py_BuildValue("i", CA_EXTRACT_MSG_NO(status));
  }
}

static PyObject *
Py_sg_put(PyObject *self, PyObject *args){
  long count;
  int status=0;
  CA_SYNC_GID gid;
  chid ch_id;
  size_t size;
  PyObject *value;
  chtype type;
  void *pbuf=NULL;

  if(!PyArg_ParseTuple(args,"illOl",&gid,&ch_id,&pbuf,&value,&type)){
    return NULL;
  }

  if(gid < 0){
    PyErr_SetString(CaError, "Null sync group ID as an argument");
    return NULL;
  }
  if( ! PySequence_Check(value) ){
    Py_XDECREF(value);
    return NULL;
  }

  Check_Connection(ch_id, "Py_sg_put"); /* MACRO for channel connection checking */

  if (type < 0){
    type=dbf_type_to_DBR(ca_field_type(ch_id));
  }

  if(!pbuf){
    count=ca_element_count(ch_id);
    size=dbr_size_n(count,dbf_type_to_DBR(ca_field_type(ch_id)))
      +dbr_size_n(1,dbf_type_to_DBR_TIME(ca_field_type(ch_id))) ;
    pbuf=malloc(size);
    if(!pbuf){
      PyErr_NoMemory();
      return NULL;
    }
  }
  
  count=PyObject_Length(value); /* just ignore data longer than channel data type */
  count=(count < ca_element_count(ch_id)?count:ca_element_count(ch_id));
  if (count < 0){
    PyErr_SetString(CaError, "invalid data length");
    return NULL;
  }

  status=_convert_Py_to_ca(type, count,
			   value, pbuf);
  if(status != 0){
    return NULL;
  }
  {ENTER_CA
    status=ca_sg_array_put(gid, type, count, ch_id, pbuf );
    SEVCHK(status, "Py_sg_array_put");
  LEAVE_CA}

  if (status != ECA_NORMAL){
    PyErr_SetString(CaError, ca_message(status));
    return NULL;
  }
  else {
    return Py_BuildValue("l",  pbuf);
  }
}

static PyObject *
Py_sg_get(PyObject *self, PyObject *args){

  int status=0,retry=0;
  CA_SYNC_GID gid;
  long type,count;
  chid ch_id;
  void *pbuf=NULL;
  size_t size;

  if(!PyArg_ParseTuple(args,"ill",&gid, &ch_id, &pbuf)){
    return NULL;
  }

  Check_Connection(ch_id,"Py_sg_get"); /* MACRO for channel connection checking */

  while( ca_state(ch_id) != cs_conn ) {
    retry++;
    {ENTER_CA
	ca_pend_io(0.1); /* wait for ch_id to connect */
    LEAVE_CA}
    if (retry > CA_MAX_RETRY){
      PyErr_SetString(CaError, "Exceed Max retry to connect.");
      return NULL;
    }
  }

  type=dbf_type_to_DBR_TIME(ca_field_type(ch_id));
  count=ca_element_count(ch_id);
  if(!pbuf){
    size=dbr_size_n(count,dbf_type_to_DBR(ca_field_type(ch_id)))
      +dbr_size_n(1,dbf_type_to_DBR_TIME(ca_field_type(ch_id))) ;
    pbuf=malloc(size);
    if(!pbuf){
      PyErr_NoMemory();
      return NULL;
    }
  }
  {ENTER_CA
      status=ca_sg_array_get(gid, type, count, ch_id, pbuf);
      SEVCHK(status, "Py_sg_array_get");
  LEAVE_CA}

  if (status != ECA_NORMAL){
    PyErr_SetString(CaError, ca_message(status));
    return NULL;
  }
  else {
    return Py_BuildValue("l",  pbuf);
  }
}

static PyObject *
Py_ca_convert(PyObject *self, PyObject *args){
  
  int status=0;
  chid ch_id;
  void *pbuf;
  PyObject *pobj;

  if(!PyArg_ParseTuple(args,"ll",&ch_id,&pbuf)){
    return NULL;
  }

  if(!ch_id  || !pbuf){
    PyErr_SetString(CaError, "Invalid Argument value(s)");
    return NULL;
  }

  pobj=_convert_ca_to_Python(dbf_type_to_DBR_TIME(ca_field_type(ch_id)),
			     ca_element_count(ch_id), 
			     pbuf, status);

  if(pobj){
    return pobj;
  }
  else{
    PyErr_SetString(CaError, "Invalid CA Values");
    return NULL;
  }
}

#define SgMoveValuesToBuffer(DBRBUFTYPE, DBRTYPE, FORMAT) \
      {\
         DBRTYPE *ptr=(DBRTYPE *) pbuf;\
	 DBRBUFTYPE buf;\
	 for(cur=0;cur<count;cur++){\
           item=PySequence_GetItem(value,cur);\
           PyArg_Parse(item,FORMAT, &buf);\
           Py_XDECREF(item);\
           ptr[cur]=(DBRTYPE) buf;\
       }}

static int
_convert_Py_to_ca(chtype type,long count, PyObject *value, void *pbuf){
  PyObject *item;
  long cur;

  if (pbuf ==(void *) NULL){
    return -1;
  }
  switch(type){
  case DBR_STRING:
    {
      register dbr_string_t *pstr=(dbr_string_t *) pbuf;
      char *str;
      for (cur=0; cur< count; cur++){
	item=PySequence_GetItem(value,cur);
	PyArg_Parse(item,"z",&str);
	Py_XDECREF(item);
	strncpy((char *)&(pstr[cur]), str, sizeof(dbr_string_t));
      }
    }
    break;
  case DBR_INT:/* note that SgMoveValuesToBuffer is Macro */
    SgMoveValuesToBuffer(dbr_long_t, dbr_int_t, "i"); 
    break;
  case DBR_FLOAT:
    SgMoveValuesToBuffer(dbr_double_t, dbr_float_t, "d");
    break;
  case DBR_ENUM:
    SgMoveValuesToBuffer(dbr_long_t, dbr_enum_t, "l");
    break;
  case DBR_CHAR:
    SgMoveValuesToBuffer(dbr_char_t,dbr_char_t,"b");
    break;
  case DBR_LONG:
    SgMoveValuesToBuffer(dbr_long_t,dbr_long_t,"l");
    break;
  case DBR_DOUBLE:
    SgMoveValuesToBuffer(dbr_double_t,dbr_double_t,"d");
    break;
  default:
    PyErr_SetString(CaError,"Invalid field type");
    return -1;
  }
  return 0;
}

/******************** end of sync. group routines *************************/

#include <signal.h>

/* fdmgr or similar routines should be used here. Noboru */
/* Yeah, so I have done it. NY */

typedef void (*signal_handler)(int);

static struct sigaction oact;
static struct sigaction act;

static void alarm_handler(int arg){

  ENTER_CA
    ca_pend_event(CA_PEND_EVENT_TIME);
  LEAVE_CA
  /*   if (oact.sa_handler != ((void( *)(int)) NULL) ) */
  /*     oact.sa_handler(arg); */
  ualarm(CA_POLL_INTERVAL,NULL);
}

static void setup_alarm(void){
  int status;

  sigaction(SIGALRM,NULL,&oact);

  act.sa_handler=alarm_handler;
  act.sa_mask =oact.sa_mask ;
  /* act.sa_flags=oact.sa_flags & ~SA_RESETHAND;*/
  act.sa_flags=0;/* we don't want old behaviour */
  status=sigaction(SIGALRM,&act,&oact);
  if (status != 0) perror("set_alarm");
  ualarm(CA_POLL_INTERVAL,NULL);
}

static void stop_alarm(void){
  struct sigaction act;
  act.sa_handler=alarm_handler;
 
  sigaction(SIGALRM,&oact,NULL);
  ualarm(CA_POLL_INTERVAL,NULL);
}

static PyObject *Py_start_alarm(PyObject *self, PyObject *args)
{
  setup_alarm();
  Py_INCREF(Py_None);
  return Py_None;

}

static PyObject *Py_stop_alarm(PyObject *self, PyObject *args)
{
  stop_alarm();
  Py_INCREF(Py_None);
  return Py_None;
}


static void Py_ca_fd_register(void *pfdctx, int fd, int condition)
{
#if defined(WITH_TK) && ! defined(WITH_THREAD)
  if(condition){
    Tk_CreateFileHandler(fd, TK_READABLE, Py_ca_service, pfdctx);
  }
  else{
    Tk_DeleteFileHandler(fd);
  }
#endif
}

/*
******************************************************
* NAME
*	Py_ca_service()
* DESCRIPTION
*	1) call ca_pend_event to allow event handler execution
******************************************************
* Note: Feb. 2, 2000 by NY
* This function will be called from Tcl interpreter, which
* set tcl_lock and has NULL Python-thread state.
*/
static void Py_ca_service()
{
#if 0
  struct timeval tp,tp1;
  struct timezone tzp;
  gettimeofday(&tp1, &tzp);
#endif

#if 0
  fprintf(stderr, "in ca_service ... ");fflush(stderr);
#endif
  ENTER_CA{
    /*ca_pend_event(CA_PEND_EVENT_TIME);*/
    ca_poll();
  }LEAVE_CA;
#if 0
    fprintf(stderr, "done!\n");fflush(stderr);	  
#endif
#if 0
  gettimeofday(&tp1, &tzp);
  printf(" %d %d\n", tp.tv_sec, tp.tv_usec);
  printf(" %d %d\n", tp1.tv_sec, tp1.tv_usec);
#endif
}

/* alternative exception handler for EPICS/CA */
static void exceptionCallback(struct exception_handler_args args)
{
  if (args.chid && args.op != CA_OP_OTHER) {
    exceptionCallbackFormated(
			      args.stat,
			      args.pFile,
			      args.lineNo,
			      "%s - with request chan=%s op=%ld data type=%s count=%ld",
			      args.ctx,
			      ca_name (args.chid),
			      args.op,
			      dbr_type_to_text(args.type),
			      args.count);
  }
  else {
    exceptionCallbackFormated(
			      args.stat,
			      args.pFile,
			      args.lineNo,
			      args.ctx);
  }
}

static int exceptionCallbackFormated(long ca_status, const char *pfilenm,
				 int lineno, const char *pFormat,
				 ...)
{
  va_list             theArgs;
  static const char   *severity[] =
  { "Warning",
    "Success",
    "Error",
    "Info",
    "Fatal",
    "Fatal",
    "Fatal",
    "Fatal"
  };
  
  va_start (theArgs, pFormat);
  
  errlogPrintf ("CA.Client.Diagnostic.................................\n");

  errlogPrintf ("    %s: \"%s\"\n",
		severity[CA_EXTRACT_SEVERITY(ca_status)],
		ca_message (ca_status));

  if  (pFormat) {
    errlogPrintf ("    Context: \"");
    errlogVprintf (pFormat, theArgs);
    errlogPrintf ("\"\n");
  }
  
  if (pfilenm) {
    errlogPrintf("Source File: %s Line Number: %d\n",
		 pfilenm,
		 lineno);
  }
  
  errlogPrintf(".....................................................\n");
  va_end (theArgs);
  
  return 0;

}
