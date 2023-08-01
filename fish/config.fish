if status is-interactive
    # Commands to run in interactive sessions can go here
    if status is-interactive


        if set -q VIM
            # Using from vim/neovim.
            set onedark_options -256
        else if string match -iq "eterm*" $TERM
            # Using from emacs.
            function fish_title
                true
            end
            set onedark_options -256
        end
    end
    set c /home/jadong/.config
    alias asciiapp="python3 ~/asciiapp.py"
    alias python="bash ~/mypython.sh"
    alias i3lockj="i3lock --blur 10 -k  --{time, date,greeter}-color=#cad3f5FF --{time, date, layout, verif, wrong, greeter}-font=JetBrainsMonoNerdFont --{time, layout, greeter}-size=76 --radius=80 --{inside, ring}-color=#ed8796	--{key, bs}hl-color=#8bd5caca"
end
asciiapp --color
starship init fish | source
