#include <stdio.h>
#include <unistd.h>
#include <errno.h>

int main()
{
    int rc = 0;
    pid_t pid = 0;
    int x = 100;
    pid = fork();
    if(pid == 0)
    {
        x = 200;
        printf("The value of x is %d\n", x);
        printf("This is the child process with pid %u\n", getpid());
    }
    else if(pid > 0)
    {
        x = 300;
        printf("This is the value of the variable x in parent %d\n", x);
        printf("This is the parent process with pid: %u\n", getpid());
        printf("The child was created was PID %u\n", pid);
    }
    else 
    {
        printf("Fork failed with error code: %d", pid);
    }
    return 0;
}