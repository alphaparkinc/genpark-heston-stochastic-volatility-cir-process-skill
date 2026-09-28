"""MCP stdio server for Heston Model."""
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import HestonSimulator

def handle_rpc(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "simulate_heston",
                        "description": "Simulate Heston stochastic volatility paths with Feller condition checking",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "s0": {"type": "number"},
                                "v0": {"type": "number"},
                                "mu": {"type": "number"},
                                "kappa": {"type": "number"},
                                "theta": {"type": "number"},
                                "xi": {"type": "number"},
                                "rho": {"type": "number"},
                                "steps": {"type": "integer", "default": 50},
                                "seed": {"type": "integer", "default": 42}
                            },
                            "required": ["s0", "v0", "mu", "kappa", "theta", "xi", "rho"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "simulate_heston":
            res = HestonSimulator.simulate_paths(
                s0=float(args.get("s0")),
                v0=float(args.get("v0")),
                mu=float(args.get("mu")),
                kappa=float(args.get("kappa")),
                theta=float(args.get("theta")),
                xi=float(args.get("xi")),
                rho=float(args.get("rho")),
                t_max=float(args.get("t_max", 1.0)),
                steps=int(args.get("steps", 50)),
                seed=int(args.get("seed", 42))
            )
            return {"jsonrpc": "2.0", "id": req_id, "result": res}
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {name} not found"}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Invalid request"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_rpc(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
