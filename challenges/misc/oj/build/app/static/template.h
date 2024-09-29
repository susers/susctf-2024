#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <seccomp.h>

#include <vector>
#include <iostream>
using namespace std;

{{ code }}

int main() {
    vector<vector<int>> envelopes = {{5,4},{6,4},{6,7},{2,3}};
    char buffer[1024];

    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fstat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(mmap), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(brk), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(ioctl), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(writev), 0);
    seccomp_load(ctx);
    seccomp_release(ctx);

    Solution s;
    int r = s.maxEnvelopes(envelopes);

    cout << r << endl;
    return 0;
}