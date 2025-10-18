export type DemoProfile = {
  id: number;
  platform: string;
  handle: string;
  display_name: string;
  avatar_url: string | null;
  bio: string | null;
  sample_posts: { posts: string[] } | null;
};



