# zeaz-platform tunnel — ID: 45667e7e-7383-4265-b53e-6a9e770a8554
# Credentials: /home/zeazdev/.cloudflared/45667e7e-7383-4265-b53e-6a9e770a8554.json
# Config:      /home/zeazdev/.cloudflared/config.yml
# Service:     systemd cloudflared (protocol: http2)

resource "cloudflare_tunnel" "zeaz_tunnel" {
  account_id = var.account_id
  name       = "zeaz-tunnel"
  secret     = var.tunnel_secret # stored in tfvars / env secret
}

resource "cloudflare_tunnel_config" "zeaz_tunnel_config" {
  account_id = var.account_id
  tunnel_id  = cloudflare_tunnel.zeaz_tunnel.id

  config {
    origin_request {
      http2_origin        = true
      no_tls_verify       = false
      connect_timeout     = "10s"
      tls_timeout         = "10s"
      keep_alive_timeout  = "1m30s"
    }

    # ─── Identity ──────────────────────────────────────────────────────────────
    ingress_rule {
      hostname = "auth.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }

    # ─── AI Platform ───────────────────────────────────────────────────────────
    ingress_rule {
      hostname = "zveo.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "api-zveo.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "zstudio.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "analytics.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }

    # ─── Financial Platform ─────────────────────────────────────────────────────
    ingress_rule {
      hostname = "app.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "zpay.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "ztreasury.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "zwallet.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }

    # ─── Developer Tools & Cockpits ────────────────────────────────────────────
    ingress_rule {
      hostname = "zcloud.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "zdash.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "api-zdash.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "zcfdash.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "api-zcfdash.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "release.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }

    # ─── Algo Trading & Game Services ──────────────────────────────────────────
    ingress_rule {
      hostname = "ztrader.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "api-ztrader.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "zcino.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }

    # ─── Educational & Workspace Portals ───────────────────────────────────────
    ingress_rule {
      hostname = "zacademy.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "academy.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "zlms.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "zoffice.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "zow.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }

    # ─── Automation ────────────────────────────────────────────────────────────
    ingress_rule {
      hostname = "zfbauto.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }

    # ─── Agent UI (direct bypass traefik) ──────────────────────────────────────
    ingress_rule {
      hostname = "zagents.zeaz.dev"
      service  = "http://172.18.0.1:3009"
    }

    # ─── Root & API ────────────────────────────────────────────────────────────
    ingress_rule {
      hostname = "www.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "zeaz.dev"
      service  = "http://172.18.0.3:80"
    }
    ingress_rule {
      hostname = "api.zeaz.dev"
      service  = "http://172.18.0.3:80"
    }

    # ─── Wildcard catch-all subdomains → traefik ───────────────────────────────
    ingress_rule {
      service = "http://172.18.0.3:80"
    }
  }
}
