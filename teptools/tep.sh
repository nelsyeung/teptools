#!/usr/bin/env bash
#
# Main teptools script to be sourced.
TEPTOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEPTOOLS_SCRIPTS="$(find "$TEPTOOLS_DIR" -maxdepth 1 -name "*.py" -prune -o \
					-name "*.pyc" -prune -o \
					-name "__pycache__" -prune -o \
					-name "tep.sh" -prune -o \
					-name ".__version__" -prune -o \
					-type f -name "*" -exec basename {} \; | tr '\n' ' ')"
export TEPTOOLS_DIR TEPTOOLS_SCRIPTS


##################################################
# Main teptools function
#
# Finds the correct script from the input arguments
# or use default action if not found
# then execute the script along with the rest of the arguments
#
# Globals:
#   TEPTOOLS_DIR
#   TEPTOOLS_SCRIPTS
# Arguments:
#   None
# Returns:
#   None
##################################################
tep() {
	local scripts="$TEPTOOLS_SCRIPTS"
	local script=""
	local default_action="$(_tep_default_action)"
	local fuzzy_search=""
	local args_index=2

	if [[ $# -eq 0 ]]; then
		if [[ -z $default_action ]]; then
			_tep_print_help
			return
		fi

		script=$default_action
	else
		script=$1
	fi

	fuzzy_search=$(_tep_fuzzy_search $script true)

	# If the argument is an option of the script (e.g., --output)
	# or if fuzzy search didn't find anything (e.g., a file name input)
	# then use the default action instead.
	if [[ $script == -* || -z $fuzzy_search ]]; then
		script="$default_action"
		args_index=1

		if [[ -z $script ]]; then
			_tep_print_help
			return
		fi
	else
		script="$fuzzy_search"
	fi

	"$TEPTOOLS_DIR/$script" "${@:$args_index}"
}


_tep_print_help() {
	version=$(cat "$TEPTOOLS_DIR/.__version__")

	cat <<HERE
+---------------------------------------------------------------------+
|                                                                     |
|    ####### ####### ######  #######   #####   #####  #      #####    |
|       #    #       #     #    #     #     # #     # #     #         |
|       #    #       #     #    #     #     # #     # #     #         |
|       #    #####   ######     #     #     # #     # #      ####     |
|       #    #       #          #     #     # #     # #          #    |
|       #    #       #          #     #     # #     # #          #    |
|       #    ####### #          #      #####   #####  ###### ####     |
|                                                                     |
|                      Utility tools for ONETEP                       |
|                                                                     |
|                        Author: Nelson Yeung                         |
|                                                      Version $version  |
|                                                                     |
+---------------------------------------------------------------------+
|                                                                     |
|  Check the repository for full documentations and issues logging:   |
|                https://github.com/nelsyeung/teptools                |
|                                                                     |
|       If you have any issues but don't have a GitHub account,       |
|         you can email Nelson Yeung at n.yeung@warwick.ac.uk         |
|                                                                     |
+---------------------------------------------------------------------+
HERE
}


##################################################
# Get default action from users config file
#
# Globals:
#   None
# Arguments:
#   None
# returns:
#   script -- the default script set by the user to be executed
##################################################
_tep_default_action() {
	local rcfile="$HOME/.teptoolsrc"
	local script=""

	if [[ -f $rcfile ]]; then
		script="$(grep "action" "$rcfile" | cut -d "=" -f 2 | tr -d "[[:space:]]")"

		# Check for comments within value
		if [[ $script == *#* ]]; then
			script="$(echo $script | cut -d "#" -f 1 | tr -d "[[:space:]]")"
		fi

		echo "$script"
	fi
}


##################################################
# Fuzzy search on script name
#
# Globals:
#   TEPTOOLS_SCRIPTS
# Arguments:
#   input -- user input
#   first_match_only -- whether to break after the first match (default false)
# Returns:
#   match -- scripts that matched the fuzzy search
##################################################
_tep_fuzzy_search() {
	local input="$1"
	local first_match_only="$2"
	local fuzzy_str="^"
	local match=""

	for ((i=0; i < ${#input}; i++)); do
		fuzzy_str="$fuzzy_str${input:$i:1}.*"
	done

	for script in $TEPTOOLS_SCRIPTS; do
		if [[ $script =~ $fuzzy_str ]]; then
			match="$match $script"

			if [[ $first_match_only = true ]]; then
				break
			fi
		fi
	done

	match="$(echo "$match" | sed -e "s/^[[:space:]]*//")"

	echo "$match"
}


##################################################
# Bash autocomplete for the tep function
#
# Each argument has its own autocomplete:
# 1 -- a script from the teptools directory
# 2 -- when starts with "--", autocomplete with Python argparse arguments,
#      and back to default otherwise
#
# Globals:
#   TEPTOOLS_SCRIPTS
# Arguments:
#   None
# Returns:
#   None
##################################################
_tep_autocomplete() {
	local scripts="$TEPTOOLS_SCRIPTS"
	local cur="${COMP_WORDS[COMP_CWORD]}"
	local script="${COMP_WORDS[1]}"
	local reply=""

	if [[ $COMP_CWORD -eq 1 ]]; then
		reply="$(compgen -W "$scripts" -- $cur)"

		if [[ -z $reply ]]; then
			reply="$(_tep_fuzzy_search $cur)"
			COMPREPLY=($(compgen -W "$reply"))
		else
			COMPREPLY=($reply)
		fi
	elif [[ $COMP_CWORD -gt 1 ]]; then
		if [[ $cur == --* ]]; then
			script="$(_tep_fuzzy_search $script true)"

			if [[ $script == "summarise" ]]; then
				local options=""

				for option in $(grep -oE "\-\-[a-z-]+" "$TEPTOOLS_DIR/$script"); do
					options="$options $option"
				done

				COMPREPLY=($(compgen -W "$options" -- $cur))
			fi
		else
			COMPREPLY=($(compgen))
		fi
	fi
}

complete -o default -F _tep_autocomplete tep
