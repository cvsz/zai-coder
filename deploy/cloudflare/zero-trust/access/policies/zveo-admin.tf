resource "cloudflare_access_policy" "zveo_admin" {
  account_id     = var.account_id
  application_id = var.application_id
  name           = "zveo-admin"
  precedence     = 1
  decision       = "allow"
  include {
    group = [cloudflare_access_group.zveo_admin.id]
  }
}

resource "cloudflare_access_group" "zveo_admin" {
  account_id = var.account_id
  name       = "zveo-admin"
  include {
    email = ["admin@zeaz.dev"]
  }
}
