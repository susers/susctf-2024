#include <fcntl.h>
#include <microhttpd.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <time.h>

#include "incbin.h"

INCBIN(INDEX, "index.html");

char comments[4096];
char comment_arr[4][1024] = {"<p>Comment</p>", 0, 0, 0};
char flag[64] = "susctf{test}";
int port = 8080;

static void comment_bot() {
  int i;
  // reset flag
  for (i = 0; i < 4; i++) {
    if (comment_arr[i] && strstr(comment_arr[i], flag)) {
      memset(comment_arr[i], 0, 1024);
    }
  }
  char command[1024];
  snprintf(command, sizeof(command),
           "xvfb-run -a xterm -e \"w3m -header 'Nonce: %s' "
           "'http://localhost:%d/?commentText=%s'\"",
           flag, port, flag);
  pid_t pid = fork();
  if (pid == 0) {
    system(command);
    exit(0);
  } else if (pid > 0) {
    // xfvb pools status 3s per time, so sleep after it fully idles
    sleep(4);
    kill(pid, SIGKILL);
  } else {
    perror("fork");
  }
}

static void concat_comments(char *comments, char comment_arr[4][1024],
                            const char *nonce) {
  int i;
  memset(comments, 0, 4096);
  for (i = 0; i < 4; i++)
    if (comment_arr[i]) {
      if (strstr(comment_arr[i], flag) &&
          ((nonce && 0 != strcmp(nonce, flag)) || !nonce))
        continue;
      else
        strncat(comments, comment_arr[i], strlen(comment_arr[i]));
    }
};

static int try_add_comment(char comment_arr[4][1024], const char *comment) {
  int i;
  for (i = 0; i < 4; i++) {
    if (0 == strcmp(comment_arr[i], "")) {
      strcat(comment_arr[i], "<p>");
      strncat(comment_arr[i], comment, strlen(comment));
      strcat(comment_arr[i], "</p>");
      return MHD_YES;
    }
  }
  return MHD_NO;
}

static enum MHD_Result ahc_echo(void *cls, struct MHD_Connection *connection,
                                const char *url, const char *method,
                                const char *version, const char *upload_data,
                                size_t *upload_data_size, void **ptr) {
  static int dummy;
  char index[8192] = {0};

  struct MHD_Response *response;
  int ret;

  if (0 != strcmp(method, MHD_HTTP_METHOD_GET))
    return MHD_NO;
  if (&dummy != *ptr) {
    *ptr = &dummy;
    return MHD_YES;
  }
  if (0 != *upload_data_size)
    return MHD_NO;
  *ptr = NULL;

  const char *nonce =
      MHD_lookup_connection_value(connection, MHD_HEADER_KIND, "Nonce");
  const char *commentText = MHD_lookup_connection_value(
      connection, MHD_GET_ARGUMENT_KIND, "commentText");
  if (commentText) {
    try_add_comment(comment_arr, commentText);
  }

  concat_comments(comments, comment_arr, nonce);

  // printf("Comments: %s\n", comments);

  if (0 == strcmp(url, "/bot")) {
    sprintf(index, "Excuting the bot...");
    comment_bot();
  } else {
    sprintf(index, (const char *)gINDEXData, comments);
  }

  response = MHD_create_response_from_buffer(strlen(index), (void *)index,
                                             MHD_RESPMEM_PERSISTENT);
  MHD_add_response_header(response, "Content-Type", "text/html; charset=utf-8");
  ret = MHD_queue_response(connection, MHD_HTTP_OK, response);
  MHD_destroy_response(response);
  return ret;
}

int main(int argc, char **argv) {
  struct MHD_Daemon *d;
  if (argc != 2) {
    printf("%s PORT\n", argv[0]);
    return 1;
  }

  const char *f = getenv("GZCTF_FLAG");
  if (f)
    strcpy(flag, f);

  port = atoi(argv[1]);
  d = MHD_start_daemon(MHD_USE_THREAD_PER_CONNECTION, port, NULL, NULL,
                       &ahc_echo, NULL, MHD_OPTION_END);
  if (d == NULL)
    return 1;
  printf("Server running on %d.\n", port);
  // looping...
  while (1)
    (void)getc(stdin);
  MHD_stop_daemon(d);
  return 0;
}
