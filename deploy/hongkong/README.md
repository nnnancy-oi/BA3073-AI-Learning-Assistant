# Hong Kong HTTPS deployment snapshot

The application is derived from https://github.com/bnbu-busa-projects/AI_Learning_Assistant . Task1 changes are in backend/pipelines/essay_html.py and the exact student email-domain validator/tests.

These are the actual Nginx/auth-sidecar configuration templates used for the assignment. Application backend and authentication service publish only127.0.0.1:14242 and127.0.0.1:8082; Nginx exposes80/443. Replace hostnames, paths and certificate locations for another installation. The SSO configuration is redacted: generate a new private signing key and bcrypt password locally on the server; never use placeholder values as credentials or commit the resulting secret file.

The Cookie-based identity layer was chosen because application API requests already use Authorization:Bearer. Both UI and API require auth_request. This is simple local proxy access control, separate from the application's teaching-grade campus login.

Task3 uses an independently created Hong Kong server; the original Hangzhou Task2check remains separately submitted. Public addresses can change after stop/start: update the controlled DNS A record. Certificate renewal uses Certbot HTTP-01 webroot with an unauthenticated challenge location and a deploy hook to validate/reload Nginx.

No API keys, passwords, auth hashes, session cookies, SSH keys, databases, generated workspaces, environment files or dependencies are included in this snapshot.
