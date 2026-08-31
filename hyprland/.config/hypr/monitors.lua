-- See https://wiki.hypr.land/Configuring/Basics/Monitors/
-- List current monitors and supported resolutions with: hyprctl monitors all

local omarchy_gdk_scale = 1
local omarchy_monitor_scale = 1.25

hl.env("GDK_SCALE", tostring(omarchy_gdk_scale))
-- hl.monitor({ output = "", mode = "preferred", position = "auto", scale = omarchy_monitor_scale })

--
local handle = io.popen("hostname")
local hostname = handle:read("*a"):gsub("%s+", "") -- read output and strip whitespace/newlines
handle:close()

-- Conditionally load the host-specific configuration
if hostname == "js-t480" then
  require("monitors-t480")
elseif hostname == "js-xps8700" then
  require("monitors-xps8700")
else
  require("monitors-default")
end
