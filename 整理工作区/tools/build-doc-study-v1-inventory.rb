#!/usr/bin/env ruby
# frozen_string_literal: true

require "csv"
require "fileutils"
require "json"
require "pathname"

WORKSPACE = File.expand_path("../..", __dir__)
OLD_ROOT = File.join(WORKSPACE, "doc-study-v1")
OUTPUT_ROOT = File.join(WORKSPACE, "整理工作区")
PROBLEMS_PATH = File.join(WORKSPACE, "学习文库", "算法学习", "problems.json")

ALGORITHM_DOMAINS = {
  "搜索和回溯" => "搜索与回溯",
  "题" => "单题资料",
  "栈专题" => "栈",
  "字符串专题" => "字符串",
  "动态规划专题" => "动态规划",
  "学习方法" => "学习方法",
  "数组专题" => "数组",
  "单调栈" => "单调栈",
  "栈和哈希表" => "栈与哈希表",
  "二叉树专题" => "二叉树",
  "链表专题" => "链表",
  "基础认知" => "基础认知",
  "算法优化思想" => "算法优化",
  "学习产出" => "学习产出",
  "QA" => "历史问答"
}.freeze

META_DOMAINS = {
  ".trae" => "仓库元数据",
  "docsify" => "仓库元数据",
  "trae话术" => "仓库元数据",
  "临时QA" => "仓库元数据"
}.freeze

SEPARATE_DOMAINS = {
  "网络协议专题" => "网络协议",
  "框架" => "框架"
}.freeze

HIGH_VALUE_TOPIC_MARKERS = [
  "原理详解",
  "结构原理",
  "结构分类",
  "应用场景",
  "体系总结",
  "结构特性",
  "记忆方法",
  "通用模板",
  "万能公式",
  "万能代码",
  "通用解题方案",
  "解题模式与通用框架",
  "状态转移方程推导",
  "算法学习总结与方法论",
  "核心理解与学习心得",
  "知识点梳理",
  "题目分类梳理",
  "分类指南",
  "专栏分析",
  "专题分析",
  "哨兵元素深度解析",
  "DP概念详解",
  "DP空间优化",
  "二维DP空间优化",
  "区间DP推导",
  "递归栈模拟结构",
  "表达式栈结构",
  "状态栈结构",
  "栈+哈希表结构",
  "双栈结构",
  "基础栈结构",
  "单调栈结构"
].freeze

MIGRATE_OLD_ONLY_IDS = [
  10, 17, 19, 22, 31, 32, 39, 64, 85, 96, 104, 105, 114, 121, 141,
  142, 148, 150, 152, 160, 198, 208, 221, 224, 232, 234, 240, 279, 283,
  297, 301, 309, 312, 337, 338, 341, 399, 406, 416, 437, 438, 448, 461,
  494, 496, 538, 543, 581, 617, 621, 636, 647, 1249
].freeze

MIGRATED_IDS = [32, 150, 224, 232, 301, 1249].freeze

FOUNDATIONAL_IDS = [
  10, 17, 19, 22, 31, 32, 39, 64, 85, 96, 104, 105, 114, 121, 141, 142,
  148, 150, 152, 160, 198, 208, 221, 224, 232, 234, 240, 279, 283, 297,
  301, 309, 312, 337, 338, 341, 399, 406, 416, 437, 438, 448, 494, 496,
  538, 543, 581, 617, 621, 636, 647, 1249
].freeze

NAVIGATION_MARKERS = %w[
  README index 导航 目录 索引 汇总 总览 学习顺序 学习路径 分类速查
].freeze

def read_text(path)
  File.read(path, encoding: "UTF-8", invalid: :replace, undef: :replace)
end

def normalize_title(text)
  value = text.to_s.dup
  value = value.sub(/\.(md|java)\z/i, "")
  value = value.sub(/^(问题|题解)\d+(?:\.\d+)*[-_. ]*/i, "")
  value = value.sub(/^LeetCode[-_ ]?\d+[-_ ]*/i, "")
  value = value.sub(/\s*\(1\)\z/i, "")
  value = value.gsub(/(?:Java版本|Java小白版|逐行解释|完整实现|层序搜索|层级搜索|DFS剪枝回溯|回溯计数法|DFS三色法|Kahn算法|思路整理|深度解析|详解|说明|总结)\z/i, "")
  value.gsub(/[\s._\-()（）【】\[\]，,：:；;、|+]+/, "").downcase
end

def title_from_problem_path(relative_path)
  relative_path.split(File::SEPARATOR).each do |part|
    match = part.match(/\ALeetCode[-_ ]?(\d+)[-_ ]+(.+?)\.(?:md|java)\z/i)
    return [match[1].to_i, match[2]] if match
  end

  nil
end

def path_ids(relative_path)
  relative_path.scan(/LeetCode[-_ ]?(\d+)/i).flatten.map(&:to_i).uniq
end

def text_ids(text)
  text.scan(/LeetCode(?:\s*[-_ ]\s*)?(\d{1,4})\b/i).flatten.map(&:to_i).uniq
end

def top_directory(relative_path)
  relative_path.split(File::SEPARATOR).first
end

def parent_directory(relative_path)
  File.dirname(relative_path).split(File::SEPARATOR).last
end

def topic_label(relative_path)
  parts = relative_path.split(File::SEPARATOR)
  return parts[0] if parts.length < 2

  parts[0, [parts.length - 1, 3].min].join("/")
end

def high_value_topic?(relative_path)
  HIGH_VALUE_TOPIC_MARKERS.any? { |marker| relative_path.include?(marker) }
end

def content_type(relative_path, extension)
  basename = File.basename(relative_path)
  return "资源图片" if extension.match?(/\A(jpe?g|png|gif|webp|svg)\z/i)
  return "旧版Java实现" if extension == "java"
  return "仓库生成文件" if relative_path.start_with?(".trae/", "docsify/") ||
                           basename.match?(/\A(_sidebar|_coverpage|generate_sidebar|index\.html)/)
  return "导航索引" if basename.match?(/(?:README|index|导航|目录|索引|汇总|总览|学习顺序|学习路径)/i)
  return "微模板与易错点" if basename.include?("微模板与易错点")
  return "问题档案" if basename.start_with?("问题")
  return "题解档案" if basename.start_with?("题解")
  return "单题资料" if relative_path.start_with?("题/LeetCode-")
  return "单题资料" if path_ids(relative_path).any? && relative_path.split(File::SEPARATOR).any? { |part| part.match?(/\ALeetCode/i) }
  return "批次题解" if basename.match?(/4\.1(?:\.\d+)?/)
  return "通用原理与方法论" if high_value_topic?(relative_path)

  "其他资料"
end

def domain_for(relative_path)
  top = top_directory(relative_path)
  return META_DOMAINS.fetch(top) if META_DOMAINS.key?(top)
  return SEPARATE_DOMAINS.fetch(top) if SEPARATE_DOMAINS.key?(top)
  return "仓库元数据" if relative_path == "project_rules.md" ||
                         relative_path == "迁移溯源记录.md" ||
                         relative_path == "超级索引.md"

  ALGORITHM_DOMAINS.fetch(top, "算法其他")
end

def duplicate_role(relative_path, extension)
  return "variant" if File.basename(relative_path).match?(/\(1\)|\(2\)|副本/)
  return "generated" if content_type(relative_path, extension) == "仓库生成文件"

  "candidate"
end

def disposition_for(relative_path, extension, type, domain, primary_id, current_ids)
  return "拆分到其他资料库" if %w[网络协议 框架].include?(domain)
  return "忽略" if domain == "仓库元数据"
  return "忽略" if duplicate_role(relative_path, extension) == "variant"
  return "归档" if type == "导航索引"

  if %w[通用原理与方法论 微模板与易错点].include?(type)
    return high_value_topic?(relative_path) ? "改写后迁移" : "仅作素材"
  end

  if primary_id
    return "仅作素材" if current_ids.include?(primary_id)
    return "改写后迁移" if MIGRATE_OLD_ONLY_IDS.include?(primary_id)
    return "仅作素材"
  end

  "仅作素材"
end

def priority_for(disposition, type, primary_id, domain)
  return "P2-其他资料库" if disposition == "拆分到其他资料库"
  return "P4-忽略" if disposition == "忽略"
  return "P4-归档" if disposition == "归档"
  return "P0-通用模型" if type == "通用原理与方法论" && disposition == "改写后迁移"
  return "P1-独有题" if primary_id && !FOUNDATIONAL_IDS.include?(primary_id) && disposition == "改写后迁移"
  return "P0-独有题" if primary_id && FOUNDATIONAL_IDS.include?(primary_id) && disposition == "改写后迁移"
  return "P3-旧题素材" if primary_id
  return "P3-素材" if type == "微模板与易错点"
  return "P3-素材" if disposition == "仅作素材"

  "P3-其他"
end

def reason_for(disposition, type, primary_id, current_ids)
  case disposition
  when "拆分到其他资料库"
    "内容不属于算法标准库，应迁往更宽的资料库层级，避免污染算法五层结构。"
  when "忽略"
    "属于旧仓库元数据、生成文件、版本副本或临时内容，不进入 Obsidian 知识库。"
  when "归档"
    "仅承担旧库导航或批量索引职责，稳定导航应由当前库 README、学习看板自动替代。"
  when "改写后迁移"
    if primary_id && current_ids.include?(primary_id)
      "旧题解与当前标准题重合，只允许提取旧库独有推导后重写，不能覆盖事实与权威实现。"
    elsif primary_id
      "当前库缺失该题，可进入候选批次，但必须先补官方事实、本地示例、权威 Java 与校验。"
    else
      "跨题通用原理或方法论，适合改写为概念卡、核心模型、建模专题或 Java 速查，不直接复制。"
    end
  when "仅作素材"
    if primary_id && current_ids.include?(primary_id)
      "当前库已有完整标准题解，旧文档降为推导、错因和表达素材。"
    elsif primary_id
      "旧库独有但当前不急，先保留来源，后续按缺口和优先级决定是否重建。"
    else
      "与当前规范存在职责重叠或质量不稳定，保留为检索素材，不直接进入稳定层。"
    end
  else
    "待人工复核。"
  end
end

def target_layer_for(relative_path, type, domain, primary_id, current_problem)
  return "资料库/#{domain}" if %w[网络协议 框架].include?(domain)
  return "整理工作区归档" if domain == "仓库元数据"

  return current_problem["relativePath"] if primary_id && current_problem

  if primary_id
    return "待建：题目/<主题型>/#{primary_id}-<English-Title>.md"
  end

  return "待定：02-概念专题/栈结构模型.md" if domain == "栈" && relative_path.include?("结构")
  return "待定：02-概念专题/表达式与状态栈.md" if relative_path.include?("表达式栈") || relative_path.include?("状态栈")
  return "待定：02-概念专题/单调栈与哨兵.md" if relative_path.include?("单调栈") || relative_path.include?("哨兵")
  return "待定：02-概念专题/搜索与回溯.md" if domain == "搜索与回溯" && type == "通用原理与方法论"
  return "待定：02-概念专题/动态规划推导.md" if domain == "动态规划" && type == "通用原理与方法论"
  return "待定：Java速查/" if relative_path.include?("模板索引")

  "待人工定位"
end

problems_document = JSON.parse(File.read(PROBLEMS_PATH, encoding: "UTF-8"))
current_problems = problems_document.fetch("problems")
current_by_id = current_problems.to_h { |problem| [problem.fetch("id"), problem] }
current_ids = current_by_id.keys.to_set if defined?(Set)

require "set"
current_id_set = current_by_id.keys.to_set

old_files = Dir.glob(File.join(OLD_ROOT, "**", "*"), File::FNM_DOTMATCH)
               .select { |path| File.file?(path) }
               .sort

old_problem_titles = {}
old_files.each do |path|
  relative_path = Pathname.new(path).relative_path_from(Pathname.new(OLD_ROOT)).to_s
  parsed = title_from_problem_path(relative_path)
  next unless parsed

  id, title = parsed
  old_problem_titles[id] ||= title.sub(/\s*\(1\)\z/i, "").strip
end

all_problem_titles = current_by_id.transform_values { |problem| problem.fetch("titleCn") }
                                   .merge(old_problem_titles)

title_to_ids = Hash.new { |hash, key| hash[key] = [] }
all_problem_titles.each do |id, title|
  normalized = normalize_title(title)
  next if normalized.length < 2

  title_to_ids[normalized] << id
end

items = old_files.map do |path|
  relative_path = Pathname.new(path).relative_path_from(Pathname.new(OLD_ROOT)).to_s
  extension = File.extname(relative_path).delete_prefix(".").downcase
  text = %w[md java js py html yml yaml json txt].include?(extension) ? read_text(path) : ""
  direct_ids = path_ids(relative_path)
  referenced_ids = text_ids(text)
  title_matches = title_to_ids.fetch(normalize_title(File.basename(relative_path)), [])
  primary_id = direct_ids.one? ? direct_ids.first : (title_matches.one? ? title_matches.first : nil)
  ids = (direct_ids + referenced_ids + title_matches).uniq.sort
  type = content_type(relative_path, extension)
  domain = domain_for(relative_path)
  disposition = disposition_for(relative_path, extension, type, domain, primary_id, current_id_set)
  current_problem = primary_id ? current_by_id[primary_id] : nil

  {
    "oldRelativePath" => relative_path,
    "topDirectory" => top_directory(relative_path),
    "extension" => extension,
    "bytes" => File.size(path),
    "domain" => domain,
    "contentType" => type,
    "primaryLeetcodeId" => primary_id,
    "referencedLeetcodeIds" => ids,
    "problemTitle" => primary_id ? all_problem_titles[primary_id] : nil,
    "currentOverlap" => primary_id ? current_id_set.include?(primary_id) : false,
    "targetLayer" => target_layer_for(relative_path, type, domain, primary_id, current_problem),
    "disposition" => disposition,
    "priority" => priority_for(disposition, type, primary_id, domain),
    "reason" => reason_for(disposition, type, primary_id, current_id_set),
    "duplicateRole" => duplicate_role(relative_path, extension)
  }
end

cluster_for = lambda do |item|
  if item["primaryLeetcodeId"]
    "题:#{item["primaryLeetcodeId"]}"
  elsif %w[微模板与易错点 导航索引].include?(item["contentType"])
    "主题:#{item["domain"]}:#{topic_label(item["oldRelativePath"])}:#{normalize_title(File.basename(item["oldRelativePath"]))}"
  else
    "主题:#{normalize_title(File.basename(item["oldRelativePath"]))}"
  end
end

clusters = items.group_by { |item| cluster_for.call(item) }
clusters.each do |cluster, group|
  group.each do |item|
    item["duplicateCluster"] = cluster
    item["duplicateCount"] = group.length
  end
end

old_single_problem_ids = items.map { |item| item["primaryLeetcodeId"] }.compact.uniq.sort
overlap_ids = (old_single_problem_ids & current_id_set.to_a).sort
old_only_ids = (old_single_problem_ids - current_id_set.to_a).sort
current_only_ids = (current_id_set.to_a - old_single_problem_ids).sort

disposition_counts = items.group_by { |item| item["disposition"] }.transform_values(&:length).sort.to_h
priority_counts = items.group_by { |item| item["priority"] }.transform_values(&:length).sort.to_h
type_counts = items.group_by { |item| item["contentType"] }.transform_values(&:length).sort_by { |_, count| -count }.to_h
domain_counts = items.group_by { |item| item["domain"] }.transform_values(&:length).sort_by { |_, count| -count }.to_h
duplicate_cluster_count = clusters.count { |_, group| group.length > 1 }

summary = {
  "generatedAt" => Time.now.strftime("%Y-%m-%d"),
  "source" => {
    "repository" => "https://gitee.com/zhangdatou/doc-study-v1.git",
    "snapshotPath" => "doc-study-v1",
    "branch" => "master",
    "commit" => "777cf6ba4cf8c5b81e46df8aeeff4b2007021fac",
    "lastUpdated" => "2026-04-12",
    "gitMetadataPresent" => File.directory?(File.join(OLD_ROOT, ".git")),
    "fileCount" => items.length,
    "markdownCount" => items.count { |item| item["extension"] == "md" },
    "javaCount" => items.count { |item| item["extension"] == "java" },
    "imageCount" => items.count { |item| item["contentType"] == "资源图片" },
    "schemaV3Count" => items.count { |item| item["extension"] == "md" && read_text(File.join(OLD_ROOT, item["oldRelativePath"])).match?(/^schemaVersion:\s*3/m) },
    "duplicateClusterCount" => duplicate_cluster_count
  },
  "problemCoverage" => {
    "currentCount" => current_id_set.length,
    "oldCount" => old_single_problem_ids.length,
    "overlapCount" => overlap_ids.length,
    "oldOnlyCount" => old_only_ids.length,
    "currentOnlyCount" => current_only_ids.length,
    "overlapIds" => overlap_ids,
    "oldOnlyIds" => old_only_ids,
    "currentOnlyIds" => current_only_ids
  },
  "migrationProgress" => {
    "completedIds" => MIGRATED_IDS.select { |id| current_id_set.include?(id) },
    "completedCount" => MIGRATED_IDS.count { |id| current_id_set.include?(id) },
    "oldOnlyRemainingIds" => old_only_ids,
    "oldOnlyRemainingCount" => old_only_ids.length
  },
  "dispositionCounts" => disposition_counts,
  "priorityCounts" => priority_counts,
  "contentTypeCounts" => type_counts,
  "domainCounts" => domain_counts
}

FileUtils.mkdir_p(OUTPUT_ROOT)
inventory_path = File.join(OUTPUT_ROOT, "doc-study-v1-清单.json")
File.write(inventory_path, JSON.pretty_generate({ "summary" => summary, "items" => items }) + "\n", encoding: "UTF-8")

csv_path = File.join(OUTPUT_ROOT, "doc-study-v1-清单.csv")
CSV.open(csv_path, "w", write_headers: true, headers: items.first.keys) do |csv|
  items.each { |item| csv << item.values }
end

mapping_path = File.join(OUTPUT_ROOT, "旧新路径映射.csv")
headers = %w[
  leetcodeId 旧库题名 当前库题名 关系 迁移状态 当前标准路径 建议目标路径 迁移动作 优先级 旧库文件数 说明
]
all_mapping_ids = (old_single_problem_ids + current_only_ids).uniq.sort
old_file_count_by_id = items.group_by { |item| item["primaryLeetcodeId"] }.transform_values(&:length)

CSV.open(mapping_path, "w", write_headers: true, headers: headers) do |csv|
  all_mapping_ids.each do |id|
    current = current_by_id[id]
    relation = current && old_problem_titles.key?(id) ? "重叠" : (current ? "仅当前库" : "仅旧库")
    migrated = MIGRATED_IDS.include?(id) && current
    migration_status = if migrated
                         "首批已完成"
                       elsif relation == "仅旧库"
                         "待迁移"
                       else
                         "无需迁移"
                       end
    disposition = if migrated
                    "已完成融合"
                  elsif relation == "重叠"
                    "仅作素材"
                  elsif relation == "仅旧库"
                    MIGRATE_OLD_ONLY_IDS.include?(id) ? "改写后迁移" : "仅作素材"
                  else
                    "当前库已有"
                  end
    priority = if migrated
                 "P0-已完成"
               elsif relation == "仅旧库" && FOUNDATIONAL_IDS.include?(id)
                 "P0-优先重建"
               elsif relation == "仅旧库" && MIGRATE_OLD_ONLY_IDS.include?(id)
                 "P1-候选重建"
               elsif relation == "仅旧库"
                 "P3-素材"
               else
                 "P3-素材"
               end
    target = current ? current["relativePath"] : "题目/<主题型>/#{id}-<English-Title>.md"
    reason = if migrated
               "2026-10-04 已按 schema v3 从旧库素材重建，并加入当前 66 题主库；旧资料继续作为推导、错因和表达素材。"
             else
               case relation
             when "重叠"
               "当前库已含标准题解；旧文档只保留推导、错因和表达素材。"
             when "仅旧库"
               if FOUNDATIONAL_IDS.include?(id)
                 "基础缺口，建议优先按 schema v3 重建。"
               elsif MIGRATE_OLD_ONLY_IDS.include?(id)
                 "旧库独有且材料可重建，作为后续候选，暂不进入首批。"
               else
                 "旧库独有但当前优先级不足，先保留为检索素材。"
               end
             else
               "当前库新增题，旧库没有对应来源。"
             end
             end

    csv << [
      id,
      old_problem_titles[id],
      current&.fetch("titleCn"),
      relation,
      migration_status,
      current&.fetch("relativePath"),
      target,
      disposition,
      priority,
      old_file_count_by_id[id].to_i,
      reason
    ]
  end
end

puts "inventory=#{inventory_path}"
puts "csv=#{csv_path}"
puts "mapping=#{mapping_path}"
puts JSON.generate(summary)
