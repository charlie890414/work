# FastMCP Skill-Compatible MCP Server Scaffold

這個專案提供一個基於 **FastMCP** 的 MCP Server 架構範本，重點包含：

- 支援 function-based tool 與 group-based tool 組織方式
- Token 生成與驗證工具
- 在 server 內部提供可重用的驗證層，便於 skill server 擴充
- 提供 CLI 產 token / 驗 token（含預設值）

## 結構

- `server/main.py`：FastMCP server 入口
- `server/auth/`：Token 產生與驗證邏輯
- `server/tools/`：工具註冊（function/group）
- `server/tools/groups/`：group 拆分目錄，避免單檔過長
- `server/cli/token_cli.py`：token CLI
- `server/config.py`：設定管理

## 快速開始

1. 安裝相依：
   - `fastmcp`
   - `pyjwt`
2. 啟動：
   - `python -m server.main`

## Token CLI（有預設值）

- 產 token（全部可省略用預設）：
  - `python -m server.cli.token_cli generate`
- 指定 subject/scopes/ttl：
  - `python -m server.cli.token_cli generate --subject alice --scopes read,profile:read --ttl-seconds 7200`
- 驗 token：
  - `python -m server.cli.token_cli verify --token <JWT>`

預設值：
- `subject=dev-user`
- `scopes=read`
- `ttl_seconds=MCP_TOKEN_DEFAULT_TTL`（預設 3600）

## 如果 class 下面工具太多，怎麼拆？

建議做法：
1. 每個 domain 一個 group class（例如 `skill_group.py`, `admin_group.py`）
2. group class 內再切成 `self._register_xxx()` 私有方法，減少單一函式長度
3. 在 `server/tools/group_tools.py` 集中聚合 register，當作唯一入口
4. 共用 auth、schema、service 放到 `server/auth/` 或 `server/services/`

這樣可以在工具數量增加時維持可讀性與可測試性。

## 安全建議

- 請改用環境變數覆蓋 `MCP_SECRET_KEY`
- 若要進入正式環境，建議加上 key rotation 與 token revocation 機制
