from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', psql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(100)),
        sa.Column('last_name', sa.String(100)),
        sa.Column('organization_id', psql.UUID(as_uuid=True)),
        sa.Column('role', sa.String(50), default='user'),
        sa.Column('last_login', sa.TIMESTAMP())
    )
    op.create_table(
        'monitors',
        sa.Column('id', psql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('method', sa.String(10), nullable=False),
        sa.Column('headers', psql.JSONB),
        sa.Column('body', sa.Text()),
        sa.Column('timeout', sa.Integer()),
        sa.Column('interval_minutes', sa.Integer()),
        sa.Column('expected_status_codes', psql.ARRAY(sa.Integer)),
        sa.Column('organization_id', psql.UUID(as_uuid=True)),
        sa.Column('created_by', psql.UUID(as_uuid=True)),
        sa.Column('tags', psql.ARRAY(sa.Text)),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('group', sa.String(100)),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.func.now())
    )
    op.create_table(
        'monitor_results',
        sa.Column('id', psql.UUID(as_uuid=True), primary_key=True),
        sa.Column('monitor_id', psql.UUID(as_uuid=True), sa.ForeignKey('monitors.id')),
        sa.Column('response_time_ms', sa.Integer()),
        sa.Column('status_code', sa.Integer()),
        sa.Column('success', sa.Boolean()),
        sa.Column('error_message', sa.Text()),
        sa.Column('response_size', sa.Integer()),
        sa.Column('location', sa.String(100)),
        sa.Column('checked_at', sa.TIMESTAMP(), server_default=sa.func.now()),
        sa.Column('ssl_expiry_date', sa.TIMESTAMP())
    )
    op.create_table(
        'incidents',
        sa.Column('id', psql.UUID(as_uuid=True), primary_key=True),
        sa.Column('monitor_id', psql.UUID(as_uuid=True), sa.ForeignKey('monitors.id')),
        sa.Column('started_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('ended_at', sa.TIMESTAMP()),
        sa.Column('root_cause', sa.Text()),
        sa.Column('duration_seconds', sa.Integer())
    )

def downgrade():
    op.drop_table('incidents')
    op.drop_table('monitor_results')
    op.drop_table('monitors')
    op.drop_table('users')