# FastMCP Skill-Compatible MCP Server Scaffold

這個專案提供一個基於 **FastMCP** 的 MCP Server 架構範本，重點包含：

- 支援 function-based tool 與 group-based tool 組織方式
- Token 生成與驗證工具
- 在 server 內部提供可重用的驗證層，便於 skill server 擴充

## 結構

- `server/main.py`：FastMCP server 入口
- `server/auth/`：Token 產生與驗證邏輯
- `server/tools/`：工具註冊（function/group）
- `server/config.py`：設定管理

## 快速開始

1. 安裝相依：
   - `fastmcp`
   - `pyjwt`
2. 啟動：
   - `python -m server.main`

## 安全建議

- 請改用環境變數覆蓋 `MCP_SECRET_KEY`
- 若要進入正式環境，建議加上 key rotation 與 token revocation 機制
