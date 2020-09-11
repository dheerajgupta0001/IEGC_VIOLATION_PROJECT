call nssm.exe install mis_viol_msgs_service "%cd%\run_server.bat"
call nssm.exe set mis_viol_msgs_service AppStdout "%cd%\logs\mis_viol_msgs_service.log"
call nssm.exe set mis_viol_msgs_service AppStderr "%cd%\logs\mis_viol_msgs_service.log"
call sc start mis_viol_msgs_service