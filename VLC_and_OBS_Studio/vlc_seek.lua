require 'common'

function descriptor()
 return { title = "Seek to second 3" ;
  version = "0.1" ;
  author = "mDw" ;
  shortdesc = "Seek to second 3.";
  description = "Seek to second 3." ;
  capabilities = { "input-listener" }
 }
end

function activate()
	vlc.msg.dbg("[Seek] Activate")
end
function close()
	vlc.msg.dbg("[Seek] Close")
end
function deactivate()
	vlc.msg.dbg("[Seek] Deactivate")
end

-- Triggers
function input_changed()
	vlc.msg.dbg("[Seek] Input changed")
	goTo()
end

function meta_changed()
	vlc.msg.dbg("[Seek] Meta changed")
	goTo()
end

function goTo()
	common.seek("0h0m3s")
end

function hide_dialog()
 pathdialog:hide()
end