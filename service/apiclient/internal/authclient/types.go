package authclient

type TokenMetadataDict struct {
	UUID        string `json:"uuid"`
	TenantUUID  string `json:"tenant_uuid"`
	AuthID      string `json:"auth_id"`
	PbxUserUUID string `json:"pbx_user_uuid"`
	AccentUUID  string `json:"accent_uuid"`
}

type TokenMetadataStackDict struct {
	TokenMetadataDict
	Purpose string `json:"purpose,omitempty"`
	Admin   string `json:"admin,omitempty"`
}

type TokenDict struct {
	Token         string            `json:"token"`
	SessionUUID   string            `json:"session_uuid"`
	Metadata      TokenMetadataDict `json:"metadata"`
	ACL           []string          `json:"acl"`
	AuthID        string            `json:"auth_id"`
	AccentUUID    string            `json:"accent_uuid"`
	ExpiresAt     string            `json:"expires_at"`
	UtcExpiresAt  string            `json:"utc_expires_at"`
	IssuedAt      string            `json:"issued_at"`
	UtcIssuedAt   string            `json:"utc_issued_at"`
	UserAgent     string            `json:"user_agent"`
	RemoteAddr    string            `json:"remote_addr"`
}
