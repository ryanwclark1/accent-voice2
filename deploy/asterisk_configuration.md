# Asterisk Configuration

Contains the asterisk configurations to be located in /etc/asterisk

asterisk.conf must include allow for exec

accent-asterisk-config.conf
Executes the confgen client, which in turn calls the congen service to return the /etc/asterisk/modules.conf

## extension


```ini
include pbxconfig.conf
include /etc/accent/asterisk/accent_globals.conf

[accent-callbackdisa]
exten = s,1,DISA(no-password,${ACCENT_DISACONTEXT})
same  =   n,Hangup()

; Forged contexts and macros are included here.
exec /usr/bin/accent-confgen asterisk/extensions.conf

; Various subroutines.
include extensions_extra.d/*
include /usr/share/accent-config/dialplan/asterisk/*
```

## extensions confgen example


```ini
exten = c28bad10-66cc-4a94-b32c-c58ea54194cd,hint,Custom:c28bad10-66cc-4a94-b32c-c58ea54194cd-mobile
exten = e088ac2b-226d-46e3-bb42-c65e93e5c7fe,hint,Custom:e088ac2b-226d-46e3-bb42-c65e93e5c7fe-mobile

[ctx-accent-incall-33f214df-95e4-49a9-82d7-6d218fee48cc]
exten = i,1,Playback(no-user-find)
same = n,Hangup()
exten = s,1,NoOp()
same = n,GotoIf($[${CHANNEL(channeltype)} = PJSIP]?:not-pjsip)
same = n,GotoIf($["${ACCENT_DID_NEXT_EXTEN}" = ""]?:error-loop)
same = n,Set(ACCENT_DID_NEXT_EXTEN=${CUT(CUT(PJSIP_HEADER(read,To),@,1),:,2)})
same = n,Set(ACCENT_FROM_S=1)
same = n,Goto(ctx-accent-incall-33f214df-95e4-49a9-82d7-6d218fee48cc,${ACCENT_DID_NEXT_EXTEN},1)
same = n(not-pjsip),NoOp()
same = n,Log(ERROR, This s extension can only be used from a PJSIP channel)
same = n,Hangup()
same = n(error-loop),NoOp()
same = n,Log(ERROR, Dialplan loop detected. Got PJSIP header To: ${PJSIP_HEADER(read,To)})
same = n,Hangup()
exten = _+.,1,Goto(${EXTEN:1},1)



[ctx-accent-internal-47f8cc37-d2c2-4ec6-bc11-7f7bba437fec]
include = accent-features
include = accent-extrafeatures
include = parkedcalls
include = accent-meeting-user
exten = t,1,Hangup()
exten = i,1,Playback(no-user-find)
same = n,Hangup()



[ctx-accent-others-ddbbc3b9-6e5f-445f-af43-04266dc95942]
exten = i,1,Playback(no-user-find)
same = n,Hangup()



[ctx-accent-outcall-426c1f94-1b57-435c-9162-65d42f2349c3]



[ctx-accent-services-bfe6d9e0-f0a5-458b-a87a-4af1164f7e4c]
exten = i,1,Playback(no-user-find)
same = n,Hangup()



[ctx-None-incall-11a9dbeb-715a-4bc0-8587-d0d75e5491d1]
exten = i,1,Playback(no-user-find)
same = n,Hangup()
exten = s,1,NoOp()
same = n,GotoIf($[${CHANNEL(channeltype)} = PJSIP]?:not-pjsip)
same = n,GotoIf($["${ACCENT_DID_NEXT_EXTEN}" = ""]?:error-loop)
same = n,Set(ACCENT_DID_NEXT_EXTEN=${CUT(CUT(PJSIP_HEADER(read,To),@,1),:,2)})
same = n,Set(ACCENT_FROM_S=1)
same = n,Goto(ctx-None-incall-11a9dbeb-715a-4bc0-8587-d0d75e5491d1,${ACCENT_DID_NEXT_EXTEN},1)
same = n(not-pjsip),NoOp()
same = n,Log(ERROR, This s extension can only be used from a PJSIP channel)
same = n,Hangup()
same = n(error-loop),NoOp()
same = n,Log(ERROR, Dialplan loop detected. Got PJSIP header To: ${PJSIP_HEADER(read,To)})
same = n,Hangup()
exten = _+.,1,Goto(${EXTEN:1},1)



[ctx-None-internal-a4e57e63-ded4-402d-8094-1ec214dd2bfc]
include = accent-features
include = accent-extrafeatures
include = parkedcalls
include = accent-meeting-user
exten = t,1,Hangup()
exten = i,1,Playback(no-user-find)
same = n,Hangup()



[ctx-None-others-4a3d9bbb-d522-49e5-93e2-2d7638c8a72f]
exten = i,1,Playback(no-user-find)
same = n,Hangup()



[ctx-None-outcall-ce80af91-4cdd-4719-9763-6198b8aa0c88]



[ctx-None-services-9ad53569-7050-42c0-aaf5-9aa8f88bbbcd]
exten = i,1,Playback(no-user-find)
same = n,Hangup()


[accent-features]
exten = *10,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(phonestatus,s,1())

exten = _*11.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(paging,s,1(${EXTEN:3}))

exten = *20,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(fwdundoall,s,1())

exten = _*21.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(feature_forward,s,1(unc,${EXTEN:3}))

exten = _*22.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(feature_forward,s,1(rna,${EXTEN:3}))

exten = _*23.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(feature_forward,s,1(busy,${EXTEN:3}))

exten = *25,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(enablednd,s,1())

exten = *27,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(incallfilter,s,1())

exten = _*30.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(agentstaticlogtoggle,s,1(${EXTEN:3}))

exten = _*31.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(agentstaticlogin,s,1(${EXTEN:3}))

exten = _*32.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(agentstaticlogoff,s,1(${EXTEN:3}))

exten = *36,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,Directory(${CONTEXT})

exten = _*37.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(bsfilter,s,1(${EXTEN:3}))

exten = *40,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(cctoggle,s,1())

exten = _*41.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(meetingjoin,s,1(${EXTEN:3}))

exten = *48378,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(autoprov,s,1())

exten = _*50.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(group-member-toggle,s,1(${EXTEN:3}))

exten = _*51.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(group-member-join,s,1(${EXTEN:3}))

exten = _*52.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(group-member-leave,s,1(${EXTEN:3}))

exten = _*735.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(phoneprogfunckey,s,1(${EXTEN:0:4},${EXTEN:4}))

exten = *9,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(recsnd,s,1(wav))

exten = *90,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(enablevm,s,1())

exten = _*90.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(enablevm,s,1(${EXTEN:3}))

exten = _*96.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(vmuser,s,1(${EXTEN:3}))

exten = _*97.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(vmbox,s,1(${EXTEN:3}))

exten = *98,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(vmusermsg,s,1())

exten = _*99.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(vmboxmsg,s,1(${EXTEN:3}))

exten = *23,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
exten = *23,n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
exten = *23,n,Gosub(feature_forward,s,1(busy))
exten = *22,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
exten = *22,n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
exten = *22,n,Gosub(feature_forward,s,1(rna))
exten = *21,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
exten = *21,n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
exten = *21,n,Gosub(feature_forward,s,1(unc))
[accent-ivr-1]
exten = s,1,Set(IVR_COUNTER=0)
same  =   n,Gosub(accent-pickup,0,1)
same  =   n,Background(vm-Urgent)
same  =   n(start),Set(IVR_COUNTER=$[${IVR_COUNTER} + 1])
same  =   n,Background(tt-monkeys)
same  =   n,WaitExten(5)




exten = t,1,NoOp()
same  =   n,GotoIf($[${IVR_COUNTER}>=3]?abort,1)
same  =   n,Goto(s,start)

exten = i,1,NoOp()
same  =   n,Gosub(forward,s,1(extension,3533,accent-incall))


exten = abort,1,NoOp()
same  =   n,Playback(error-sorry)
same  =   n,Hangup()

[usersharedlines]
exten = c28bad10-66cc-4a94-b32c-c58ea54194cd,hint,Custom:c28bad10-66cc-4a94-b32c-c58ea54194cd-mobile
exten = e088ac2b-226d-46e3-bb42-c65e93e5c7fe,hint,Custom:e088ac2b-226d-46e3-bb42-c65e93e5c7fe-mobile

[ctx-accent-incall-33f214df-95e4-49a9-82d7-6d218fee48cc]
exten = i,1,Playback(no-user-find)
same = n,Hangup()
exten = s,1,NoOp()
same = n,GotoIf($[${CHANNEL(channeltype)} = PJSIP]?:not-pjsip)
same = n,GotoIf($["${ACCENT_DID_NEXT_EXTEN}" = ""]?:error-loop)
same = n,Set(ACCENT_DID_NEXT_EXTEN=${CUT(CUT(PJSIP_HEADER(read,To),@,1),:,2)})
same = n,Set(ACCENT_FROM_S=1)
same = n,Goto(ctx-accent-incall-33f214df-95e4-49a9-82d7-6d218fee48cc,${ACCENT_DID_NEXT_EXTEN},1)
same = n(not-pjsip),NoOp()
same = n,Log(ERROR, This s extension can only be used from a PJSIP channel)
same = n,Hangup()
same = n(error-loop),NoOp()
same = n,Log(ERROR, Dialplan loop detected. Got PJSIP header To: ${PJSIP_HEADER(read,To)})
same = n,Hangup()
exten = _+.,1,Goto(${EXTEN:1},1)



[ctx-accent-internal-47f8cc37-d2c2-4ec6-bc11-7f7bba437fec]
include = accent-features
include = accent-extrafeatures
include = parkedcalls
include = accent-meeting-user
exten = t,1,Hangup()
exten = i,1,Playback(no-user-find)
same = n,Hangup()



[ctx-accent-others-ddbbc3b9-6e5f-445f-af43-04266dc95942]
exten = i,1,Playback(no-user-find)
same = n,Hangup()



[ctx-accent-outcall-426c1f94-1b57-435c-9162-65d42f2349c3]



[ctx-accent-services-bfe6d9e0-f0a5-458b-a87a-4af1164f7e4c]
exten = i,1,Playback(no-user-find)
same = n,Hangup()



[ctx-None-incall-11a9dbeb-715a-4bc0-8587-d0d75e5491d1]
exten = i,1,Playback(no-user-find)
same = n,Hangup()
exten = s,1,NoOp()
same = n,GotoIf($[${CHANNEL(channeltype)} = PJSIP]?:not-pjsip)
same = n,GotoIf($["${ACCENT_DID_NEXT_EXTEN}" = ""]?:error-loop)
same = n,Set(ACCENT_DID_NEXT_EXTEN=${CUT(CUT(PJSIP_HEADER(read,To),@,1),:,2)})
same = n,Set(ACCENT_FROM_S=1)
same = n,Goto(ctx-None-incall-11a9dbeb-715a-4bc0-8587-d0d75e5491d1,${ACCENT_DID_NEXT_EXTEN},1)
same = n(not-pjsip),NoOp()
same = n,Log(ERROR, This s extension can only be used from a PJSIP channel)
same = n,Hangup()
same = n(error-loop),NoOp()
same = n,Log(ERROR, Dialplan loop detected. Got PJSIP header To: ${PJSIP_HEADER(read,To)})
same = n,Hangup()
exten = _+.,1,Goto(${EXTEN:1},1)



[ctx-None-internal-a4e57e63-ded4-402d-8094-1ec214dd2bfc]
include = accent-features
include = accent-extrafeatures
include = parkedcalls
include = accent-meeting-user
exten = t,1,Hangup()
exten = i,1,Playback(no-user-find)
same = n,Hangup()



[ctx-None-others-4a3d9bbb-d522-49e5-93e2-2d7638c8a72f]
exten = i,1,Playback(no-user-find)
same = n,Hangup()



[ctx-None-outcall-ce80af91-4cdd-4719-9763-6198b8aa0c88]



[ctx-None-services-9ad53569-7050-42c0-aaf5-9aa8f88bbbcd]
exten = i,1,Playback(no-user-find)
same = n,Hangup()


[accent-features]
exten = *10,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(phonestatus,s,1())

exten = _*11.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(paging,s,1(${EXTEN:3}))

exten = *20,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(fwdundoall,s,1())

exten = _*21.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(feature_forward,s,1(unc,${EXTEN:3}))

exten = _*22.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(feature_forward,s,1(rna,${EXTEN:3}))

exten = _*23.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(feature_forward,s,1(busy,${EXTEN:3}))

exten = *25,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(enablednd,s,1())

exten = *27,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(incallfilter,s,1())

exten = _*30.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(agentstaticlogtoggle,s,1(${EXTEN:3}))

exten = _*31.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(agentstaticlogin,s,1(${EXTEN:3}))

exten = _*32.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(agentstaticlogoff,s,1(${EXTEN:3}))

exten = *36,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,Directory(${CONTEXT})

exten = _*37.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(bsfilter,s,1(${EXTEN:3}))

exten = *40,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(cctoggle,s,1())

exten = _*41.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(meetingjoin,s,1(${EXTEN:3}))

exten = *48378,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(autoprov,s,1())

exten = _*50.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(group-member-toggle,s,1(${EXTEN:3}))

exten = _*51.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(group-member-join,s,1(${EXTEN:3}))

exten = _*52.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(group-member-leave,s,1(${EXTEN:3}))

exten = _*735.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(phoneprogfunckey,s,1(${EXTEN:0:4},${EXTEN:4}))

exten = *9,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(recsnd,s,1(wav))

exten = *90,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(enablevm,s,1())

exten = _*90.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(enablevm,s,1(${EXTEN:3}))

exten = _*96.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(vmuser,s,1(${EXTEN:3}))

exten = _*97.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(vmbox,s,1(${EXTEN:3}))

exten = *98,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(vmusermsg,s,1())

exten = _*99.,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
same  =     n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
same  =     n,GoSub(contextlib,entry-exten-context,1)
same  =     n,GoSub(vmboxmsg,s,1(${EXTEN:3}))

exten = *23,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
exten = *23,n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
exten = *23,n,Gosub(feature_forward,s,1(busy))
exten = *22,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
exten = *22,n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
exten = *22,n,Gosub(feature_forward,s,1(rna))
exten = *21,1,Set(__ACCENT_BASE_CONTEXT=${CONTEXT})
exten = *21,n,Set(__ACCENT_BASE_EXTEN=${EXTEN})
exten = *21,n,Gosub(feature_forward,s,1(unc))
[accent-ivr-1]
exten = s,1,Set(IVR_COUNTER=0)
same  =   n,Gosub(accent-pickup,0,1)
same  =   n,Background(vm-Urgent)
same  =   n(start),Set(IVR_COUNTER=$[${IVR_COUNTER} + 1])
same  =   n,Background(tt-monkeys)
same  =   n,WaitExten(5)




exten = t,1,NoOp()
same  =   n,GotoIf($[${IVR_COUNTER}>=3]?abort,1)
same  =   n,Goto(s,start)

exten = i,1,NoOp()
same  =   n,Gosub(forward,s,1(extension,3533,accent-incall))


exten = abort,1,NoOp()
same  =   n,Playback(error-sorry)
same  =   n,Hangup()
```

# extensions - includes
/usr/share/accent-config/dialplan/asterisk/
extensions_callme.conf
extensions_lib_agents.conf
extensions_lib_applications.conf
extensions_lib_conferences.conf
extensions_lib_contexts.conf
extensions_lib_did.conf
extensions_lib_features.conf
extensions_lib_group.conf
extensions_lib_ivr.conf
extensions_lib_meeting.conf
extensions_lib_originate.conf
extensions_lib_outcall.conf
extensions_lib_paging.conf
extensions_lib_pre_dial.conf
extensions_lib_queues.conf
extensions_lib_statis.conf
extensions_lib_subr.conf
extensions_lib_switchboard.conf
extensions_lib_user.conf
extensions_lib_vmbox.conf


