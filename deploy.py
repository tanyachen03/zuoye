#!/usr/bin/env python3
import requests
import json
import base64
import os

GITHUB_TOKEN = "ghp_DqdLO4kfOhjyA82jJAn9weLOnezKw43EaND"
REPO_OWNER = "tanyachen03"
REPO_NAME = "xinde"
BRANCH = "main"

def get_current_commit_sha():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/ref/heads/{BRANCH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["object"]["sha"]
    else:
        print(f"Error getting current commit: {response.status_code}")
        print(response.text)
        return None

def get_tree_sha():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/main?recursive=1"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["sha"]
    return None

def get_file_content(filepath):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["sha"]
    return None

def update_file(filepath, content, message, sha=None):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    data = {
        "message": message,
        "content": encoded_content,
        "branch": BRANCH
    }
    
    if sha:
        data["sha"] = sha
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"✓ Updated: {filepath}")
        return True
    else:
        print(f"✗ Failed to update {filepath}: {response.status_code}")
        print(response.text)
        return False

def deploy():
    print("🚀 开始部署到 GitHub Pages...")
    
    commit_sha = get_current_commit_sha()
    if not commit_sha:
        print("无法获取当前提交")
        return
    
    print(f"当前分支: {BRANCH}")
    print(f"提交SHA: {commit_sha[:8]}")
    
    projects_dir = "/workspace/data-analytics-platform/projects"
    files_to_update = [
        "projects/project2.html",
        "projects/project3.html",
        "projects/project4.html",
        "projects/project5.html",
        "projects/project6.html",
        "projects/project7.html",
        "projects/project8.html",
        "projects/project9.html",
        "projects/project10.html"
    ]
    
    print("\n📤 上传修复后的文件...")
    success_count = 0
    
    for filepath in files_to_update:
        full_path = os.path.join("/workspace/data-analytics-platform", filepath)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_sha = get_file_content(filepath)
            if update_file(filepath, content, f"修复 {filepath} - 恢复编辑器功能", file_sha):
                success_count += 1
        else:
            print(f"✗ 文件不存在: {filepath}")
    
    print(f"\n✅ 部署完成！成功上传 {success_count}/{len(files_to_update)} 个文件")
    print("🌐 请访问: https://tanyachen03.github.io/xinde/")

if __name__ == "__main__":
    deploy()
