import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tuitlog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'static/uploads/photos')
app.config['AVATAR_FOLDER'] = os.environ.get('AVATAR_FOLDER', 'static/uploads/avatars')
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16777216))
app.config['ALLOWED_EXTENSIONS'] = set(os.environ.get('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif').split(','))

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# ============================================================================
# MODELOS DE DADOS
# ============================================================================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, default='')
    avatar = db.Column(db.String(256), default='default.png')
    is_pro = db.Column(db.Boolean, default=False)
    bg_color = db.Column(db.String(7), default='#fafafa')
    accent_color = db.Column(db.String(7), default='#2d5a5a')
    font_family = db.Column(db.String(50), default="'Inter', sans-serif")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    friendships_as_user1 = db.relationship('Friendship', foreign_keys='Friendship.user1_id', backref='user1', lazy='dynamic')
    friendships_as_user2 = db.relationship('Friendship', foreign_keys='Friendship.user2_id', backref='user2', lazy='dynamic')
    visits_made = db.relationship('Visit', foreign_keys='Visit.visitor_id', back_populates='visitor', lazy='dynamic')
    visits_received = db.relationship('Visit', foreign_keys='Visit.visited_user_id', back_populates='visited_user', lazy='dynamic')
    guestbook_entries = db.relationship('GuestbookEntry', foreign_keys='GuestbookEntry.owner_id', back_populates='owner', lazy='dynamic', cascade='all, delete-orphan')
    community_memberships = db.relationship('CommunityMember', back_populates='member', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_friends(self):
        friends = []
        for f in self.friendships_as_user1:
            friends.append(f.user2)
        for f in self.friendships_as_user2:
            friends.append(f.user1)
        return friends

    def is_friend_with(self, other_user):
        return Friendship.query.filter(
            ((Friendship.user1_id == self.id) & (Friendship.user2_id == other_user.id)) |
            ((Friendship.user1_id == other_user.id) & (Friendship.user2_id == self.id))
        ).first() is not None


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(256), nullable=False)
    caption = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    views = db.Column(db.Integer, default=0)
    
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user1_id', 'user2_id', name='unique_friendship'),)


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    visited_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    visitor = db.relationship('User', foreign_keys=[visitor_id], back_populates='visits_made')
    visited_user = db.relationship('User', foreign_keys=[visited_user_id], back_populates='visits_received')


class GuestbookEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    author = db.relationship('User', foreign_keys=[user_id], backref='guestbook_authored')
    owner = db.relationship('User', foreign_keys=[owner_id], back_populates='guestbook_entries')


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    creator = db.relationship('User', foreign_keys=[creator_id])
    members = db.relationship('CommunityMember', backref='community', lazy='dynamic', cascade='all, delete-orphan')


class CommunityMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    member = db.relationship('User', back_populates='community_memberships')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'community_id', name='unique_community_member'),)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_today_post(user):
    today = datetime.utcnow().date()
    return Post.query.filter(
        Post.user_id == user.id,
        db.func.date(Post.created_at) == today
    ).first()


def count_posts_today(user):
    today = datetime.utcnow().date()
    return Post.query.filter(
        Post.user_id == user.id,
        db.func.date(Post.created_at) == today
    ).count()


def record_visit(visitor, visited):
    if visitor and visitor != visited:
        visit = Visit(visitor_id=visitor.id, visited_user_id=visited.id)
        db.session.add(visit)
        db.session.commit()


# ============================================================================
# ROTAS PRINCIPAIS
# ============================================================================

@app.route('/')
def index():
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(24).all()
    
    # Ranking de Tuitlogs mais visitados nos últimos 7 dias
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    popular_users = db.session.query(
        User.id, User.username, User.display_name, User.avatar,
        db.func.count(Visit.id).label('visit_count')
    ).join(Visit, User.id == Visit.visited_user_id).filter(
        Visit.visited_at >= seven_days_ago
    ).group_by(User.id).order_by(db.func.count(Visit.id).desc()).limit(10).all()
    
    # Comunidades em destaque
    communities = Community.query.order_by(Community.created_at.desc()).limit(6).all()
    
    return render_template('index.html', 
                         recent_posts=recent_posts, 
                         popular_users=popular_users,
                         communities=communities)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        display_name = request.form.get('display_name', '').strip()
        
        if not username or not email or not password or not display_name:
            flash('Todos os campos são obrigatórios.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado.', 'error')
            return render_template('register.html')
        
        user = User(username=username, email=email, display_name=display_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Conta criada com sucesso! Faça login para começar seu Tuitlog.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Bem-vindo de volta!', 'success')
            return redirect(next_page or url_for('index'))
        
        flash('Credenciais inválidas.', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do Tuitlog.', 'info')
    return redirect(url_for('index'))


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.display_name = request.form.get('display_name', '').strip()
        current_user.bio = request.form.get('bio', '').strip()
        current_user.bg_color = request.form.get('bg_color', '#fafafa')
        current_user.accent_color = request.form.get('accent_color', '#2d5a5a')
        current_user.font_family = request.form.get('font_family', "'Inter', sans-serif")
        
        avatar = request.files.get('avatar')
        if avatar and allowed_file(avatar.filename):
            filename = secure_filename(avatar.filename)
            filename = f"{current_user.id}_{filename}"
            avatar.save(os.path.join(app.config['AVATAR_FOLDER'], filename))
            current_user.avatar = filename
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('profile', username=current_user.username))
    
    return render_template('edit_profile.html')


@app.route('/tuitlog/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    # Registrar visita
    record_visit(current_user if current_user.is_authenticated else None, user)
    
    # Foto do dia
    today_post = get_today_post(user)
    
    # Arquivo cronológico (excluindo a foto do dia se existir)
    archive_posts = Post.query.filter_by(user_id=user.id)\
        .order_by(Post.created_at.desc())\
        .all()
    if today_post:
        archive_posts = [p for p in archive_posts if p.id != today_post.id]
    
    # Amigos
    friends = user.get_friends()
    
    # Contador de visitas únicas (últimos 7 dias)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    visit_count = Visit.query.filter(
        Visit.visited_user_id == user.id,
        Visit.visited_at >= seven_days_ago
    ).count()
    
    # Comunidades do usuário
    user_communities = [cm.community for cm in user.community_memberships]
    
    is_owner = current_user.is_authenticated and current_user.id == user.id
    is_friend = False
    if current_user.is_authenticated:
        is_friend = current_user.is_friend_with(user)
    
    return render_template('profile.html',
                         user=user,
                         today_post=today_post,
                         archive_posts=archive_posts,
                         friends=friends,
                         visit_count=visit_count,
                         user_communities=user_communities,
                         is_owner=is_owner,
                         is_friend=is_friend)


@app.route('/tuit/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Incrementar visualizações
    post.views += 1
    db.session.commit()
    
    # Comentários
    comments = Comment.query.filter_by(post_id=post.id)\
        .order_by(Comment.created_at.asc())\
        .all()
    
    is_owner = current_user.is_authenticated and current_user.id == post.user_id
    
    return render_template('view_post.html', post=post, comments=comments, is_owner=is_owner)


@app.route('/postar', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        # Verificar limite para conta gratuita
        if not current_user.is_pro:
            if count_posts_today(current_user) >= 1:
                flash('Você já registrou seu momento hoje. Volte amanhã para continuar seu Tuitlog.', 'info')
                return redirect(url_for('profile', username=current_user.username))
        
        image = request.files.get('image')
        caption = request.form.get('caption', '').strip()
        
        if not image or not allowed_file(image.filename):
            flash('Por favor, selecione uma imagem válida.', 'error')
            return render_template('create_post.html')
        
        filename = secure_filename(image.filename)
        filename = f"{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        post = Post(image=filename, caption=caption, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        
        flash('Seu Tuit foi publicado com sucesso!', 'success')
        return redirect(url_for('view_post', post_id=post.id))
    
    # Verificar se já postou hoje
    already_posted = not current_user.is_pro and count_posts_today(current_user) >= 1
    
    return render_template('create_post.html', already_posted=already_posted)


@app.route('/tuit/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    text = request.form.get('text', '').strip()
    
    if not text:
        flash('O comentário não pode estar vazio.', 'error')
        return redirect(url_for('view_post', post_id=post.id))
    
    # Limite de 20 comentários por postagem para contas gratuitas
    comment_count = Comment.query.filter_by(post_id=post.id).count()
    if comment_count >= 20:
        flash('Este Tuit atingiu o limite de 20 comentários.', 'error')
        return redirect(url_for('view_post', post_id=post.id))
    
    comment = Comment(text=text, user_id=current_user.id, post_id=post.id)
    db.session.add(comment)
    db.session.commit()
    
    flash('Comentário adicionado!', 'success')
    return redirect(url_for('view_post', post_id=post.id))


@app.route('/comentario/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post = Post.query.get_or_404(comment.post_id)
    
    # Apenas o dono da postagem pode excluir comentários
    if current_user.id != post.user_id:
        flash('Apenas o dono do Tuit pode excluir comentários.', 'error')
        return redirect(url_for('view_post', post_id=post.id))
    
    db.session.delete(comment)
    db.session.commit()
    
    flash('Comentário excluído.', 'success')
    return redirect(url_for('view_post', post_id=post.id))


@app.route('/tuitlog/<username>/add_friend', methods=['POST'])
@login_required
def add_friend(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    if current_user.id == user.id:
        flash('Você não pode adicionar a si mesmo.', 'error')
        return redirect(url_for('profile', username=username))
    
    if current_user.is_friend_with(user):
        flash('Vocês já são Tuitamigos!', 'info')
        return redirect(url_for('profile', username=username))
    
    friendship = Friendship(user1_id=min(current_user.id, user.id),
                           user2_id=max(current_user.id, user.id))
    db.session.add(friendship)
    db.session.commit()
    
    flash(f'{user.display_name} agora é seu Tuitamigo!', 'success')
    return redirect(url_for('profile', username=username))


@app.route('/tuitlog/<username>/remove_friend', methods=['POST'])
@login_required
def remove_friend(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    friendship = Friendship.query.filter(
        ((Friendship.user1_id == current_user.id) & (Friendship.user2_id == user.id)) |
        ((Friendship.user1_id == user.id) & (Friendship.user2_id == current_user.id))
    ).first()
    
    if friendship:
        db.session.delete(friendship)
        db.session.commit()
        flash('Amizade removida.', 'info')
    
    return redirect(url_for('profile', username=username))


@app.route('/tuitlog/<username>/tuitbook', methods=['GET', 'POST'])
def tuitbook(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Faça login para deixar uma mensagem no Tuitbook.', 'error')
            return redirect(url_for('login'))
        
        text = request.form.get('text', '').strip()
        if not text:
            flash('A mensagem não pode estar vazia.', 'error')
            return redirect(url_for('tuitbook', username=username))
        
        entry = GuestbookEntry(text=text, user_id=current_user.id, owner_id=user.id)
        db.session.add(entry)
        db.session.commit()
        
        flash('Mensagem deixada no Tuitbook!', 'success')
        return redirect(url_for('tuitbook', username=username))
    
    entries = GuestbookEntry.query.filter_by(owner_id=user.id)\
        .order_by(GuestbookEntry.created_at.desc())\
        .all()
    
    return render_template('tuitbook.html', user=user, entries=entries)


@app.route('/tuitcomunidades')
def communities():
    all_communities = Community.query.order_by(Community.created_at.desc()).all()
    return render_template('communities.html', communities=all_communities)


@app.route('/tuitcomunidade/<int:community_id>')
def view_community(community_id):
    community = Community.query.get_or_404(community_id)
    members = [cm.member for cm in community.members]
    
    # Posts dos membros
    member_ids = [m.id for m in members]
    posts = Post.query.filter(Post.user_id.in_(member_ids))\
        .order_by(Post.created_at.desc())\
        .limit(50)\
        .all()
    
    is_member = False
    if current_user.is_authenticated:
        is_member = CommunityMember.query.filter_by(
            user_id=current_user.id, community_id=community.id
        ).first() is not None
    
    return render_template('view_community.html', 
                         community=community, 
                         members=members, 
                         posts=posts,
                         is_member=is_member)


@app.route('/tuitcomunidade/create', methods=['GET', 'POST'])
@login_required
def create_community():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('O nome da comunidade é obrigatório.', 'error')
            return render_template('create_community.html')
        
        community = Community(name=name, description=description, creator_id=current_user.id)
        db.session.add(community)
        
        # Adicionar criador como membro
        membership = CommunityMember(user_id=current_user.id, community_id=community.id)
        db.session.add(membership)
        db.session.commit()
        
        flash('Comunidade criada com sucesso!', 'success')
        return redirect(url_for('view_community', community_id=community.id))
    
    return render_template('create_community.html')


@app.route('/tuitcomunidade/<int:community_id>/join', methods=['POST'])
@login_required
def join_community(community_id):
    community = Community.query.get_or_404(community_id)
    
    existing = CommunityMember.query.filter_by(
        user_id=current_user.id, community_id=community.id
    ).first()
    
    if not existing:
        membership = CommunityMember(user_id=current_user.id, community_id=community.id)
        db.session.add(membership)
        db.session.commit()
        flash(f'Você entrou na comunidade {community.name}!', 'success')
    
    return redirect(url_for('view_community', community_id=community_id))


@app.route('/tuitcomunidade/<int:community_id>/leave', methods=['POST'])
@login_required
def leave_community(community_id):
    community = Community.query.get_or_404(community_id)
    
    membership = CommunityMember.query.filter_by(
        user_id=current_user.id, community_id=community.id
    ).first()
    
    if membership:
        db.session.delete(membership)
        db.session.commit()
        flash(f'Você saiu da comunidade {community.name}.', 'info')
    
    return redirect(url_for('view_community', community_id=community_id))


@app.route('/explorar')
def explore():
    page = request.args.get('page', 1, type=int)
    per_page = 24
    posts = Post.query.order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('explore.html', posts=posts)


# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

def create_default_user():
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@tuitlog.com',
                display_name='Administrador',
                bio='Conta oficial do Tuitlog',
                is_pro=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Usuário admin criado: admin / admin123')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_user()
    app.run(host='0.0.0.0', port=1313, debug=True)
