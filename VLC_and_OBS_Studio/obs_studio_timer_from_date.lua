obs					= obslua

path_input			= ""
source_name_output	= ""
last_text     		= ""
activated     		= false

-- Function to set the output text
function set_output_text()
	local text = "-"
	local str_date = "-"
	
	-- Read file
	local file = io.open(path_input, "r")
	if file then 
		str_date = file:read()
		file:close()
	end
	
	-- Parse the date
	local func_date = string.gmatch(str_date, "[0-9]+")
	local arr_date = {}
	local count = 0

	-- Put the date in an array
	for i in func_date do
		arr_date[count] = i
		count = count + 1
	end

	-- Check the array is correct
	if count == 6 then
		-- Compute the difference between now and the date contained in input
		local start_date = os.time({year=arr_date[0], month=arr_date[1], day=arr_date[2], hour=arr_date[3], min=arr_date[4], sec=arr_date[5]})
		local sec_diff = os.difftime(os.time(), start_date)
		
		local hours = math.floor(sec_diff / 3600)
		local mins = math.floor(sec_diff / 60 - (hours * 60))
		local secs = math.floor(sec_diff - hours * 3600 - mins * 60)
		
		text = string.format("%02.f", hours) .. ":" .. string.format("%02.f", mins) .. ":" .. string.format("%02.f", secs)
	end

	-- Update the output timer
	if text ~= last_text then
		local source_output = obs.obs_get_source_by_name(source_name_output)
		if source_output ~= nil then
			local settings_output = obs.obs_data_create()
			obs.obs_data_set_string(settings_output, "text", text)
			obs.obs_source_update(source_output, settings_output)
			obs.obs_data_release(settings_output)
			obs.obs_source_release(source_output)
		end
		last_text = text
	end
end

function timer_callback()
	set_output_text()
end

-- Function called when settings are changed or source is active
function activate(activating)
	if activated == activating then
		return
	end

	activated = activating

	if activating then
		set_output_text()
		obs.timer_add(timer_callback, 1000)
	else
		obs.timer_remove(timer_callback)
	end
end

-- Function called when a source is activated/deactivated
function activate_signal(cd, activating)
	local source = obs.calldata_source(cd, "source")
	if source ~= nil then
		local name = obs.obs_source_get_name(source)
		if (name == source_name_output) then
			activate(activating)
		end
	end
end

function source_activated(cd)
	activate_signal(cd, true)
end

function source_deactivated(cd)
	activate_signal(cd, false)
end

-- Function called when settings are changed
function reset()
	activate(false)

	local source = obs.obs_get_source_by_name(source_name_output)
	if source ~= nil then
		local active = obs.obs_source_active(source) -- A source is only considered active if it’s being shown on the final mix
		obs.obs_source_release(source)
		activate(active)
	end
end

--------------------------
-- OBS global functions --
--------------------------
-- Function to define the properties that the user can change
function script_properties()
	local props = obs.obs_properties_create()

	obs.obs_properties_add_text(props, "path_input", "Path file INPUT", obs.OBS_TEXT_DEFAULT)

	local p = obs.obs_properties_add_list(props, "source_output", "Text source OUTPUT", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
	local sources = obs.obs_enum_sources()
	if sources ~= nil then
		for _, source in ipairs(sources) do
			source_id = obs.obs_source_get_id(source)
			if source_id == "text_gdiplus" or source_id == "text_ft2_source" then
				local name = obs.obs_source_get_name(source)
				obs.obs_property_list_add_string(p, name, name)
			end
		end
	end
	obs.source_list_release(sources)

	return props
end

-- Get the description shown to the user
function script_description()
	return "Set the input date file path to act as the time reference\n(It must be ending by '/TIME_START_PLAYING.txt')\n\nSet a text source output to act as the timer.\n\nBy mDw"
end

-- Function called when settings are changed
function script_update(settings)
	activate(false)

	path_input = obs.obs_data_get_string(settings, "path_input")
	source_name_output = obs.obs_data_get_string(settings, "source_output")
	
	reset()
end

-- Function called on startup
function script_load(settings)
	local sh = obs.obs_get_signal_handler()
	obs.signal_handler_connect(sh, "source_activate", source_activated)
	obs.signal_handler_connect(sh, "source_deactivate", source_deactivated)
end
