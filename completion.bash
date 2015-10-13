_hdtv()
{
    local cur prev opts base
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    #
    #  The basic options we'll complete.
    #
    opts="--device --tuner help list view"


    #
    #  Complete the arguments to some of the basic commands.
    #
    case "${prev}" in
	view)
	    local channels=$(hdtv list | egrep '^[0-9]+-[0-9]+: ' | cut -d: -f1)
	    COMPREPLY=( $(compgen -W "${channels}" -- ${cur}) )
            return 0
            ;;
        help|list)
            COMPREPLY=(  )
            return 0
            ;;
        *)
        ;;
    esac

   COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
   return 0
}
complete -F _hdtv hdtv

#
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
