#!/usr/bin/env python3
"""不依赖 GitHub Actions，直接把构建好的站点推到 gh-pages 分支。

当 Actions 不可用（例如账户账单被锁）时用这个脚本：

    python website/deploy_pages.py                      # 构建 + 推送
    python website/deploy_pages.py --dry-run            # 只构建，不推送
    python website/deploy_pages.py --base-url https://… # 覆盖站点网址

推送后在仓库 Settings → Pages → Build and deployment → Source 选择
"Deploy from a branch"，分支选 `gh-pages` / `(root)`。

实现方式是 git worktree：把 gh-pages 分支挂到一个临时目录，整体替换内容后
提交推送，不会影响你当前的工作区和 main 分支。
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

WEBSITE_DIR = Path(__file__).resolve().parent
REPO_DIR = WEBSITE_DIR.parent
DIST_DIR = WEBSITE_DIR / "dist"
BRANCH = "gh-pages"


def run(args, cwd=REPO_DIR, check=True, capture=False):
    result = subprocess.run(
        args, cwd=str(cwd), check=False,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
        text=True,
    )
    if check and result.returncode != 0:
        if capture and result.stdout:
            print(result.stdout)
        sys.exit("命令失败（退出码 %d）：%s" % (result.returncode, " ".join(args)))
    return result


def remote_url() -> str:
    out = run(["git", "remote", "get-url", "origin"], capture=True).stdout.strip()
    return out


def default_base_url() -> str:
    """从 origin 推导 https://<owner>.github.io/<repo>。"""
    url = remote_url()
    tail = url.split("github.com", 1)[-1].lstrip(":/")
    owner, _, repo = tail.partition("/")
    if repo.endswith(".git"):
        repo = repo[:-4]
    return "https://%s.github.io/%s" % (owner.lower(), repo)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="", help="站点网址，默认从 origin 推导")
    parser.add_argument("--dry-run", action="store_true", help="只构建，不推送")
    args = parser.parse_args()

    base_url = args.base_url or default_base_url()
    print("站点网址：%s" % base_url)

    run([sys.executable, str(WEBSITE_DIR / "build.py"), "--clean", "--base-url", base_url])
    if not (DIST_DIR / "index.html").exists():
        sys.exit("构建产物缺少 index.html，已中止。")
    if args.dry_run:
        print("--dry-run：已构建但未推送。")
        return

    # gh-pages 分支可能还不存在：本地先建一个孤立分支。
    exists = run(["git", "rev-parse", "--verify", "--quiet", BRANCH],
                 check=False, capture=True).returncode == 0
    tmp = Path(tempfile.mkdtemp(prefix="ai4m-pages-"))
    worktree = tmp / BRANCH
    try:
        if exists:
            run(["git", "worktree", "add", str(worktree), BRANCH])
        else:
            run(["git", "worktree", "add", "--orphan", "-b", BRANCH, str(worktree)])

        # 清空旧内容（保留 .git 指针文件），再铺上新产物。
        for item in worktree.iterdir():
            if item.name == ".git":
                continue
            shutil.rmtree(item) if item.is_dir() else item.unlink()
        shutil.copytree(DIST_DIR, worktree, dirs_exist_ok=True)

        run(["git", "add", "-A"], cwd=worktree)
        staged = run(["git", "diff", "--cached", "--quiet"], cwd=worktree,
                     check=False, capture=True).returncode != 0
        if not staged:
            print("站点内容没有变化，无需推送。")
            return
        head = run(["git", "rev-parse", "--short", "HEAD"], capture=True).stdout.strip()
        run(["git", "commit", "-q", "-m", "Deploy site from %s" % head], cwd=worktree)
        run(["git", "push", "origin", BRANCH], cwd=worktree)
        print("\n已推送到 %s 分支。" % BRANCH)
        print("在 Settings → Pages 选择 Deploy from a branch → %s / (root)，"
              "稍候即可访问：\n  %s/" % (BRANCH, base_url))
    finally:
        run(["git", "worktree", "remove", "--force", str(worktree)], check=False, capture=True)
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
