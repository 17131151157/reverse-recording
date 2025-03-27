#!/bin/bash
# ubuntu系统一键安装 mysql/MongoDB/redis
# 赋予执行权限 chmod +x install_databases.sh
# 以 root 权限运行 sudo ./install_databases.sh
set -e  # 出错时终止脚本

# 更新系统
sudo apt update && sudo apt upgrade -y

# === 安装 MySQL ===
echo "Installing MySQL..."
# 预设 MySQL root 密码（非交互式设置）
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password 121474129Nm'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password 121474129Nm'
sudo apt install -y mysql-server
sudo systemctl enable mysql
sudo systemctl start mysql

# 允许 MySQL 外网访问
echo "Configuring MySQL for external access..."
sudo sed -i 's/bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf
# 创建允许远程访问的 root 用户
sudo mysql -u root -p121474129Nm -e "CREATE USER 'root'@'%' IDENTIFIED BY '121474129Nm';"
sudo mysql -u root -p121474129Nm -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;"
sudo mysql -u root -p121474129Nm -e "FLUSH PRIVILEGES;"
sudo systemctl restart mysql

# === 安装 MongoDB ===
echo "Installing MongoDB..."
# 添加 MongoDB 官方源
wget -qO- https://www.mongodb.org/static/pgp/server-6.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb.gpg
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb.gpg ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -sc)/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl enable mongod
sudo systemctl start mongod

# 允许 MongoDB 外网访问
echo "Configuring MongoDB for external access..."
sudo sed -i 's/bindIp: 127.0.0.1/bindIp: 0.0.0.0/' /etc/mongod.conf
# 启用认证（已包含在之前的脚本中）
sudo systemctl restart mongod

# === 安装 Redis ===
echo "Installing Redis..."
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

# 允许 Redis 外网访问
echo "Configuring Redis for external access..."
sudo sed -i 's/bind 127.0.0.1/bind 0.0.0.0/' /etc/redis/redis.conf
# 确保密码已设置（已包含在之前的脚本中）
sudo systemctl restart redis-server

# === 配置防火墙 ===
echo "Opening ports in firewall..."
sudo ufw allow 3306/tcp  # MySQL
sudo ufw allow 27017/tcp # MongoDB
sudo ufw allow 6379/tcp  # Redis
sudo ufw reload

# === 验证安装 ===
echo "Verifying installations..."
echo "MySQL version: $(mysql --version)"
echo "MongoDB version: $(mongod --version | head -n 1)"
echo "Redis version: $(redis-server --version | awk '{print $2}')"

echo "安装完成！外网访问配置已生效"
echo "MySQL 端口: 3306"
echo "MongoDB 端口: 27017"
echo "Redis 端口: 6379"
echo "账号密码均为 root/121474129Nm"

