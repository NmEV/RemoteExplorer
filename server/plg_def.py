# To prevent accidental operations, protect files in critical directories
def protect_del(action_data): # Action when command executes
    import os
    protected_path = "C:/User"
    if action_data.startswith(protected_path):
        return f"禁止删除 {protected_path} 目录下的文件: {action_data}"
    try:
        os.remove(action_data)
        return f"文件已删除: {action_data}"
    except FileNotFoundError:
        return f"文件未找到: {action_data}"
    except Exception as e:
        return f"删除文件时出错: {e}"

# Register commands
plugin = {
    "del": protect_del
}