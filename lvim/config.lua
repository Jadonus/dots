lvim.plugins = {
  { "catppuccin/nvim", name = "catppuccin",
    opts = {
      flavour = "mocha",
    },
  },
 {"neanias/everforest-nvim",
  version = false,
  lazy = false,
  priority = 1000, -- make sure to load this before all the other start plugins
 },

{
  "folke/persistence.nvim",
  event = "BufReadPre", -- this will only start session saving when an actual file was opened
  opts = {
    -- add any custom options here
  }
},
}

--Example configs: https://github.com/LunarVim/starter.lvim
-- Video Tutorials: https://www.youtube.com/watch?v=sFA9kX-Ud_c&list=PLhoH5vyxr6QqGu0i7tt_XoVK9v-KvZ3m6
-- Forum: https://www.reddit.com/r/lunarvim/
-- Discord: https://discord.com/invite/Xb9B4Ny
lvim.colorscheme = "catppuccin"
lvim.transparent_window = false
lvim.builtin.lualine.on_config_done = function(lualine)
  lualine.setup {
     options = {
    icons_enabled = true,
    theme = 'auto',
    component_separators = { left = '|', right = '|'},
    section_separators = { left = '', right = ''},
    disabled_filetypes = {
      statusline = {},
      winbar = {},
    },
    ignore_focus = {},
    always_divide_middle = true,
    globalstatus = false,
    refresh = {
      statusline = 1000,
      tabline = 1000,
      winbar = 1000,
    }
  },
  sections = {
    lualine_a = {'mode'},
    lualine_b = {'branch', 'diff', 'diagnostics'},
    lualine_c = {'filename'},
    lualine_x = {'encoding', 'fileformat', 'filetype'},
    lualine_y = {'progress'},
    lualine_z = {'location'}
  },
  inactive_sections = {
    lualine_a = {},
    lualine_b = {},
    lualine_c = {'filename'},
    lualine_x = {'location'},
    lualine_y = {},
    lualine_z = {}
  },
  tabline = {},
  winbar = {},
  inactive_winbar = {},
  extensions = {}
}
end
--dashboard customizations
table.insert(lvim.builtin.alpha.dashboard.section.buttons.entries,
  { "s", "󰁯  Open Last Session", "<cmd>lua require('persistence').load()<cr>" })
lvim.builtin.alpha.dashboard.section.header.val = [[
██╗         ██╗   ██╗    ███╗   ██╗     █████╗     ██████╗     
██║         ██║   ██║    ████╗  ██║    ██╔══██╗    ██╔══██╗    
██║         ██║   ██║    ██╔██╗ ██║    ███████║    ██████╔╝    
██║         ██║   ██║    ██║╚██╗██║    ██╔══██║    ██╔══██╗    
███████╗    ╚██████╔╝    ██║ ╚████║    ██║  ██║    ██║  ██║    
╚══════╝     ╚═════╝     ╚═╝  ╚═══╝    ╚═╝  ╚═╝    ╚═╝  ╚═╝    
                                                               
      ██╗   ██╗    ██╗    ███╗   ███╗       🌙                     
      ██║   ██║    ██║    ████╗ ████║                   🚀         
      ██║   ██║    ██║    ██╔████╔██║                            
      ╚██╗ ██╔╝    ██║    ██║╚██╔╝██║              🚀              
       ╚████╔╝     ██║    ██║ ╚═╝ ██║         🚀                   
        ╚═══╝      ╚═╝    ╚═╝     ╚═╝                            
                                                          J G  
]]
vim.cmd("let g:netrw_banner = 0")
vim.cmd("let g:netrw_liststyle = 1")
lvim.builtin.which_key.mappings["cc"] = {
  ":Ex ~/.config<CR>", "Projects"
}

local nvim_lsp = require "lspconfig"
nvim_lsp.tailwindcss.setup {}

